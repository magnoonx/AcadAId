import os
import re
import shutil
import time
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import LlamaCpp
from langchain_core.documents import Document

from metrics_manager import (
    get_process_ram_gb,
    get_dir_size_mb,
    format_time_duration,
    format_disk_size,
    format_latency,
    format_speed,
    format_ram,
    save_collection_metrics,
    load_collection_metrics
)

# Directorios del proyecto
VECTOR_DBS_DIR = Path(__file__).parent / "vector_dbs"
MODELS_DIR = Path(__file__).parent / "models"
MODEL_FILE = "qwen2.5-3b-instruct-q4_k_m.gguf"

EMBEDDINGS_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class RAGEngine:
    def __init__(self, model_path: str = None):
        if model_path is None:
            model_path = str(MODELS_DIR / MODEL_FILE)
        
        self.model_path = model_path
        self._embeddings = None
        self.vector_store = None
        self.llm = None
        self.n_ctx = 8192
        self.k_retriever = 8
        self.active_collection_name: Optional[str] = None
        self.last_query_metrics: Optional[Dict[str, Any]] = None
        self.last_indexing_metrics: Optional[Dict[str, Any]] = None

    @property
    def embeddings(self):
        if self._embeddings is None:
            self._embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
        return self._embeddings

    def load_document(self, file_path: str) -> List[Document]:
        """Carga un documento según su extensión (.pdf, .docx, .txt, .md) y normaliza metadatos."""
        ext = Path(file_path).suffix.lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext in [".docx", ".doc"]:
            loader = Docx2txtLoader(file_path)
        elif ext in [".txt", ".md"]:
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Formato no soportado: {ext}")
        
        docs = loader.load()
        clean_filename = Path(file_path).name
        for doc in docs:
            doc.metadata["source"] = clean_filename
            doc.metadata["file_name"] = clean_filename
            if "page" in doc.metadata:
                try:
                    page_idx = int(doc.metadata["page"]) + 1
                    doc.metadata["page_number"] = page_idx
                    doc.metadata["page_label"] = f"Pág. {page_idx}"
                except (ValueError, TypeError):
                    doc.metadata["page_label"] = f"Pág. {doc.metadata['page']}"
            else:
                doc.metadata["page_number"] = 1
                doc.metadata["page_label"] = "Pág. 1"
        return docs

    def list_collections(self) -> List[str]:
        """Lista los nombres de las bases de datos vectoriales guardadas."""
        if not VECTOR_DBS_DIR.exists():
            return []
        return [d.name for d in VECTOR_DBS_DIR.iterdir() if d.is_dir()]

    def load_existing_collection(self, collection_name: str):
        """Carga una base de datos vectorial existente en disco por su nombre."""
        target_dir = VECTOR_DBS_DIR / collection_name
        if not target_dir.exists():
            raise FileNotFoundError(f"La colección '{collection_name}' no existe.")
        
        self.vector_store = Chroma(
            persist_directory=str(target_dir),
            embedding_function=self.embeddings
        )
        self.active_collection_name = collection_name
        self.last_indexing_metrics = load_collection_metrics(collection_name)

    def get_collection_chunks_count(self) -> int:
        """Retorna la cantidad total de fragmentos (chunks) en la colección activa."""
        if self.vector_store is not None:
            try:
                if hasattr(self.vector_store, "_collection") and hasattr(self.vector_store._collection, "count"):
                    return self.vector_store._collection.count()
            except Exception:
                pass
        if self.active_collection_name:
            metrics = load_collection_metrics(self.active_collection_name)
            if metrics and "num_chunks" in metrics:
                return int(metrics["num_chunks"])
        return 0

    def get_active_disk_size_mb(self) -> float:
        """Retorna el espacio en disco en MB de la colección ChromaDB activa."""
        if self.active_collection_name:
            target_dir = VECTOR_DBS_DIR / self.active_collection_name
            return get_dir_size_mb(target_dir)
        return 0.0

    def count_tokens(self, text: str) -> int:
        """Calcula de forma fidedigna el número de tokens de un texto."""
        if not text:
            return 0
        if hasattr(self.llm, "client") and hasattr(self.llm.client, "tokenize"):
            try:
                return len(self.llm.client.tokenize(text.encode("utf-8", errors="ignore")))
            except Exception:
                pass
        if hasattr(self.llm, "get_num_tokens"):
            try:
                return self.llm.get_num_tokens(text)
            except Exception:
                pass
        # Estimación de respaldo: 1 token ≈ 4 caracteres en promedio
        return max(1, int(len(text) / 4))

    def process_documents(self, file_paths: List[str], collection_name: str) -> int:
        """Procesa múltiples documentos, genera la base vectorial y registra métricas de indexación."""
        target_dir = VECTOR_DBS_DIR / collection_name
        if target_dir.exists():
            try:
                shutil.rmtree(target_dir)
            except Exception as e:
                print(f"Aviso al limpiar directorio vectorial: {e}")

        t_start = time.perf_counter()
        documents = []
        for fp in file_paths:
            docs = self.load_document(fp)
            documents.extend(docs)

        # Dividir textos en fragmentos (chunks)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        splits = text_splitter.split_documents(documents)

        # Crear base de datos vectorial en disco bajo la carpeta nombrada
        target_dir.mkdir(parents=True, exist_ok=True)
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=str(target_dir)
        )
        t_indexing = time.perf_counter() - t_start

        self.active_collection_name = collection_name
        disk_space_mb = get_dir_size_mb(target_dir)
        ram_gb = get_process_ram_gb()

        indexing_metrics = {
            "indexing_time_sec": round(t_indexing, 2),
            "indexing_time_formatted": format_time_duration(t_indexing),
            "num_chunks": len(splits),
            "disk_space_mb": disk_space_mb,
            "ram_usage_gb": ram_gb,
            "num_files": len(file_paths),
            "collection_name": collection_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        save_collection_metrics(collection_name, indexing_metrics)
        self.last_indexing_metrics = indexing_metrics

        return len(splits)

    def init_llm(
        self,
        n_ctx: int = 8192,
        temperature: float = 0.3,
        repeat_penalty: float = 1.08,
        max_tokens: int = 1536,
        k_retriever: int = 8,
        last_n_tokens_size: int = 64
    ):
        """Inicializa el modelo de lenguaje local con hiperparámetros estables y anti-degeneración."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"El archivo del modelo no se encuentra en {self.model_path}. Ejecuta primero download_model.py"
            )

        self.n_ctx = n_ctx
        self.k_retriever = k_retriever

        self.llm = LlamaCpp(
            model_path=self.model_path,
            n_ctx=n_ctx,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.85,
            top_k=40,
            repeat_penalty=repeat_penalty,
            last_n_tokens_size=last_n_tokens_size,
            model_kwargs={"min_p": 0.05},
            stop=[
                "<|im_end|>",
                "<|endoftext|>",
                "<|im_start|>",
                "\nPregunta:",
                "\nUser:",
                "\nUsuario:",
                "\n[FUENTE",
                "\n---"
            ],
            verbose=False,
            n_threads=4
        )

    def update_params(
        self,
        temperature: float = None,
        repeat_penalty: float = None,
        max_tokens: int = None,
        k_retriever: int = None
    ):
        """Actualiza parámetros dinámicamente sin recargar el modelo desde disco."""
        if k_retriever is not None:
            self.k_retriever = k_retriever
        if self.llm is not None:
            if temperature is not None:
                self.llm.temperature = temperature
            if repeat_penalty is not None:
                self.llm.repeat_penalty = repeat_penalty
            if max_tokens is not None:
                self.llm.max_tokens = max_tokens

    @staticmethod
    def extract_doc_source_info(doc: Document) -> Tuple[str, str]:
        """Extrae el nombre limpio del archivo y el número de página de forma robusta."""
        source_raw = doc.metadata.get("file_name") or doc.metadata.get("source") or "Documento"
        file_name = Path(str(source_raw)).name if source_raw else "Documento"
        
        if "page_label" in doc.metadata:
            page_str = str(doc.metadata["page_label"])
        elif "page_number" in doc.metadata:
            page_str = f"Pág. {doc.metadata['page_number']}"
        elif "page" in doc.metadata:
            try:
                page_str = f"Pág. {int(doc.metadata['page']) + 1}"
            except (ValueError, TypeError):
                page_str = f"Pág. {doc.metadata['page']}"
        else:
            page_str = "Pág. 1"
            
        return file_name, page_str

    def _deduplicate_chunks(self, docs: List[Document]) -> List[Document]:
        """Filtra fragmentos con alta redundancia o duplicación textual."""
        unique_docs = []
        seen_texts = []
        
        for doc in docs:
            clean = " ".join(doc.page_content.split()).lower()
            if not clean:
                continue
            
            is_duplicate = False
            for seen in seen_texts:
                if clean == seen or (len(clean) > 80 and clean in seen) or (len(seen) > 80 and seen in clean):
                    is_duplicate = True
                    break
                words_clean = set(clean.split())
                words_seen = set(seen.split())
                intersection = len(words_clean & words_seen)
                union = len(words_clean | words_seen)
                if union > 0 and (intersection / union) > 0.80:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_texts.append(clean)
                unique_docs.append(doc)
                
        return unique_docs if unique_docs else docs

    def _build_prompt(self, context: str, question: str) -> str:
        """Construye el prompt en formato ChatML con instrucciones estrictas de fidelidad y citación."""
        prompt = f"""<|im_start|>system
Eres un asistente de investigación académica riguroso. Tu objetivo es responder a la consulta del usuario basándote con máxima fidelidad en los fragmentos de documentos adjuntos.

NORMAS ESTRICTAS DE RESPUESTA Y CITACIÓN:
1. FIDELIDAD DOCUMENTAL (ANTI-ALUCINACIÓN):
   - Responde ÚNICAMENTE con hechos e información presentes de forma explícita en los fragmentos.
   - NUNCA inventes definiciones, conceptos ni atribuyas a un documento temas que no estén en sus fragmentos.
   - Si los fragmentos NO contienen información suficiente para responder la pregunta (por ejemplo, si el documento trata de otro tema o de otra época y no menciona lo consultado), debes responder honestamente:
     "Los documentos provistos no contienen información relevante sobre este tema."
   - No fuerces citas a páginas que solo contengan referencias bibliográficas o texto no relacionado.

2. CERO REPETICIÓN:
   - Desarrolla una explicación fluida y concisa, avanzando progresivamente sin reiterar ideas ni frases.
   - Concluye directamente al terminar la explicación.

3. CITAS OBLIGATORIAS POR PÁRRAFO:
   - Al final de CADA párrafo que contenga información extraída, incluye la cita exacta con el formato: `[Archivo: <nombre>, Pág. <número>]`.
   - Ejemplo:
     "El sistema implementa modelos acústicos autorregresivos para sintetizar ondas sonoras [Archivo: paper_investigacion.pdf, Pág. 5]."
   - Usa exclusivamente los archivos y páginas indicados en las fuentes provistas.

Fragmentos de los documentos:
{context}<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
"""
        return prompt

    def _find_best_source(self, text: str, docs: List[Document]) -> Tuple[str, str]:
        """Encuentra el documento más afín semánticamente al texto dado comparando términos clave."""
        if not docs:
            return "Documento", "Pág. 1"
        
        stopwords = {
            "de", "la", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no",
            "una", "su", "al", "lo", "como", "mas", "más", "pero", "sus", "le", "ya", "o", "fue", "este",
            "ha", "si", "sobre", "entre", "cuando", "tambien", "también", "hasta", "hay", "donde", "quien",
            "desde", "todos", "nos", "durante", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante",
            "ellos", "esto", "mi", "antes", "algunos", "qué", "que", "unos", "yo", "otro", "otras", "otra",
            "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "sea", "poco", "ella",
            "son", "esta", "está", "están", "estan", "puede", "pueden", "ser", "tiene", "tienen"
        }
        words = [w for w in re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]{3,}\b', text.lower()) if w not in stopwords]
        
        best_doc = docs[0]
        best_score = -1
        
        for doc in docs:
            doc_words = set(re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]{3,}\b', doc.page_content.lower()))
            score = sum(1 for w in words if w in doc_words)
            if score > best_score:
                best_score = score
                best_doc = doc
                
        return self.extract_doc_source_info(best_doc)

    def _ensure_citation(self, text: str, docs: List[Document]) -> str:
        """Garantiza que un párrafo o línea termine con [Archivo: <nombre>, Pág. <num>]."""
        tail = text[-180:] if len(text) > 180 else text
        has_page = bool(re.search(r'(?:Pág\.|Página|pag\.|pág\.|p\.)\s*\d+', tail, re.IGNORECASE))
        has_file = bool(re.search(r'\.(?:pdf|docx|doc|txt|md)', tail, re.IGNORECASE))

        # Si ya contiene archivo y página en los corchetes finales
        if has_page and has_file:
            return text

        # Si tiene el archivo pero le falta la página (ej: [Archivo: paper.pdf] o [paper.pdf])
        if has_file and not has_page:
            match = re.search(r'\[(?:Archivo:\s*|Fuente:\s*)?([^\]\n,]+?\.(?:pdf|docx|doc|txt|md))\]', text, re.IGNORECASE)
            if match:
                cited_file = match.group(1).strip()
                for doc in docs:
                    f_name, p_str = self.extract_doc_source_info(doc)
                    if Path(f_name).name.lower() == Path(cited_file).name.lower():
                        return text[:match.start()] + f"[Archivo: {f_name}, {p_str}]" + text[match.end():]

        # Si no tiene cita válida o solo tenía página sin archivo
        best_file, best_page = self._find_best_source(text, docs)
        citation = f"[Archivo: {best_file}, {best_page}]"
        
        # Si termina con corchetes incompletos (ej: [Pág. 2]), reemplazarlos
        old_cite_match = re.search(r'\s*\[[^\]\n]+\]\.?$', text)
        if old_cite_match:
            base_text = text[:old_cite_match.start()].rstrip()
            return f"{base_text} {citation}."

        # Insertar antes del punto final si existe
        if text.endswith("."):
            return f"{text[:-1].rstrip()} {citation}."
        else:
            return f"{text} {citation}"

    @staticmethod
    def _clean_degeneration_from_text(p: str) -> str:
        """Trunca el texto si detecta colapso lingüístico, bucles de caracteres o tokens rotos."""
        sentences = re.split(r'(?<=[.!?])\s+', p)
        clean_sentences = []
        for s in sentences:
            words = s.split()
            is_bad = False
            for w in words:
                # Palabras excesivamente largas sin espacio (típico de colapso de BPE)
                if len(w) > 28 and not w.startswith("http"):
                    is_bad = True
                    break
                # Letras idénticas repetidas 4 o más veces (ej: eeee, LLLL, dddd)
                if re.search(r'([a-zA-Z])\1{3,}', w):
                    is_bad = True
                    break
                # Palabras con alternancia caótica de mayúsculas/minúsculas de más de 16 caracteres
                if len(w) > 16 and sum(1 for c in w if c.isupper()) > 4 and sum(1 for c in w if c.islower()) > 4:
                    is_bad = True
                    break
            if is_bad:
                break
            clean_sentences.append(s)
        return " ".join(clean_sentences).strip()

    def _post_process_answer(self, text: str, docs: List[Document]) -> str:
        """Limpia la respuesta, elimina repeticiones, limpia artefactos y asegura citas precisas por párrafo."""
        if not text or not docs:
            return text.strip() if text else ""

        # 1. Cortar si el modelo generó secuencias de parada o turnos adicionales
        for marker in ["<|im_end|>", "<|endoftext|>", "<|im_start|>", "\nPregunta:", "\nUser:", "\nUsuario:", "\n[FUENTE", "\n---"]:
            if marker in text:
                text = text.split(marker)[0]

        text = text.strip()

        # 2. Dividir por párrafos (separados por 2 o más saltos de línea)
        raw_paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if not raw_paragraphs:
            return text

        # 3. Eliminar párrafos duplicados, artefactos o repetidos
        unique_paragraphs = []
        seen_paras = []

        for p in raw_paragraphs:
            # Descartar líneas que sean únicamente separadores o citas sueltas (ej: "--- [Archivo: ...]")
            if re.match(r'^(?:---|—|\*\*\*)\s*.*$', p) or re.match(r'^\s*\[Archivo:[^\]]+\]\s*$', p):
                continue

            cleaned_p = self._clean_degeneration_from_text(p)
            if not cleaned_p or len(cleaned_p) < 15:
                # Si el párrafo colapsó en degeneración, se detiene la lectura
                break

            norm_p = " ".join(cleaned_p.split()).lower()
            if not norm_p:
                continue

            is_dup = False
            for seen in seen_paras:
                if norm_p == seen:
                    is_dup = True
                    break
                words_p = set(norm_p.split())
                words_s = set(seen.split())
                inter = len(words_p & words_s)
                union = len(words_p | words_s)
                if union > 0 and (inter / union) > 0.85:
                    is_dup = True
                    break

            if not is_dup:
                seen_paras.append(norm_p)
                unique_paragraphs.append(cleaned_p)

        # 4. Asegurar cita [Archivo: ..., Pág. ...] al final de cada párrafo
        processed_paragraphs = []

        for p in unique_paragraphs:
            # Ignorar encabezados markdown puros
            if p.startswith("#"):
                processed_paragraphs.append(p)
                continue
            
            # Subtítulos cortos en negrita
            if len(p.splitlines()) == 1 and len(p) < 50 and p.startswith("**") and (p.endswith("**") or p.endswith(":**")):
                processed_paragraphs.append(p)
                continue

            # Declaraciones de que no se encontró información (no forzar citas a disclaimers)
            if any(phrase in p.lower() for phrase in ["no contienen información", "no se encuentra disponible", "no contienen datos", "no se menciona en los documentos"]):
                processed_paragraphs.append(p)
                continue

            # Bloques de viñetas o listas numeradas
            lines = p.splitlines()
            if len(lines) > 1 and any(line.strip().startswith(("-", "*", "•")) or re.match(r'^\d+\.', line.strip()) for line in lines):
                processed_lines = []
                for line in lines:
                    line_clean = line.strip()
                    if not line_clean:
                        continue
                    is_bullet = line_clean.startswith(("-", "*", "•")) or bool(re.match(r'^\d+\.', line_clean))
                    if is_bullet and len(line_clean) > 25:
                        processed_lines.append(self._ensure_citation(line_clean, docs))
                    else:
                        processed_lines.append(line)
                processed_paragraphs.append("\n".join(processed_lines))
                continue

            # Párrafo estándar
            processed_paragraphs.append(self._ensure_citation(p, docs))

        return "\n\n".join(processed_paragraphs)

    def ask(self, query: str) -> Dict[str, Any]:
        """Realiza una consulta a los documentos cargados con búsqueda diversa MMR y registra métricas completas."""
        if self.vector_store is None or self.llm is None:
            raise ValueError("Primero debes procesar documentos e inicializar el modelo.")

        # 1. Recuperar fragmentos utilizando MMR midiendo latencia precisa
        t_mmr_start = time.perf_counter()
        try:
            raw_docs = self.vector_store.max_marginal_relevance_search(
                query,
                k=self.k_retriever,
                fetch_k=min(self.k_retriever * 3, 30),
                lambda_mult=0.65
            )
        except Exception:
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": self.k_retriever}
            )
            raw_docs = retriever.invoke(query)
        t_mmr_end = time.perf_counter()
        mmr_latency_ms = round((t_mmr_end - t_mmr_start) * 1000, 1)

        # 2. Desduplicar fragmentos para evitar contexto redundante
        docs = self._deduplicate_chunks(raw_docs)

        # 3. Formatear fragmentos con archivo y página de forma limpia
        context_parts = []
        for i, doc in enumerate(docs, 1):
            file_name, page_str = self.extract_doc_source_info(doc)
            snippet = doc.page_content.strip()
            context_parts.append(f"[FUENTE {i} | Archivo: {file_name}, {page_str}]:\n{snippet}")
        context_str = "\n\n".join(context_parts)

        # 4. Construir prompt y generar respuesta midiendo velocidad en tokens/s
        prompt = self._build_prompt(context_str, query)
        t_gen_start = time.perf_counter()
        raw_answer = self.llm.invoke(prompt)
        t_gen_end = time.perf_counter()
        gen_time_s = max(t_gen_end - t_gen_start, 0.001)

        if hasattr(raw_answer, "content"):
            raw_text = raw_answer.content
        else:
            raw_text = str(raw_answer)

        tokens_count = self.count_tokens(raw_text)
        gen_speed = round(tokens_count / gen_time_s, 1)

        # 5. Medir consumo de RAM y almacenamiento del proyecto activo
        ram_gb = get_process_ram_gb()
        disk_mb = self.get_active_disk_size_mb()
        total_chunks = self.get_collection_chunks_count()

        # 6. Post-procesamiento estricto: eliminar duplicaciones, artefactos y asegurar citas
        clean_answer = self._post_process_answer(raw_text, docs)

        metrics = {
            "mmr_latency_ms": mmr_latency_ms,
            "gen_speed_tok_s": gen_speed,
            "tokens_generated": tokens_count,
            "gen_time_s": round(gen_time_s, 2),
            "ram_usage_gb": ram_gb,
            "disk_space_mb": disk_mb,
            "num_chunks": total_chunks,
            "k_retriever": self.k_retriever
        }
        self.last_query_metrics = metrics

        return {
            "result": clean_answer,
            "source_documents": docs,
            "metrics": metrics
        }

    def run_benchmark(
        self,
        sample_query: str = "Sintetiza los puntos clave y conceptos principales abordados en los documentos.",
        k: int = 8
    ) -> Dict[str, Any]:
        """Ejecuta una evaluación controlada en el proyecto activo para registrar los 6 parámetros del paper."""
        if self.vector_store is None:
            raise ValueError("Primero debes cargar o procesar una colección documental.")
        if self.llm is None:
            raise ValueError("El modelo de lenguaje no está inicializado.")

        # 1. Recuperar métricas de indexación guardadas si existen
        idx_metrics = load_collection_metrics(self.active_collection_name) if self.active_collection_name else None
        if idx_metrics and "indexing_time_formatted" in idx_metrics:
            indexing_time_str = idx_metrics["indexing_time_formatted"]
        elif idx_metrics and "indexing_time_sec" in idx_metrics:
            indexing_time_str = format_time_duration(idx_metrics["indexing_time_sec"])
        else:
            indexing_time_str = "Pre-indexado"

        # 2. Número de Chunks
        num_chunks = self.get_collection_chunks_count()

        # 3. Espacio en disco ChromaDB
        disk_mb = self.get_active_disk_size_mb()

        # 4. Latencia de búsqueda MMR (k = 8)
        old_k = self.k_retriever
        self.k_retriever = k
        try:
            t_mmr_start = time.perf_counter()
            raw_docs = self.vector_store.max_marginal_relevance_search(
                sample_query,
                k=k,
                fetch_k=min(k * 3, 30),
                lambda_mult=0.65
            )
            t_mmr_end = time.perf_counter()
            mmr_latency_ms = (t_mmr_end - t_mmr_start) * 1000
        except Exception:
            t_mmr_start = time.perf_counter()
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": k}
            )
            raw_docs = retriever.invoke(sample_query)
            t_mmr_end = time.perf_counter()
            mmr_latency_ms = (t_mmr_end - t_mmr_start) * 1000
        finally:
            self.k_retriever = old_k

        docs = self._deduplicate_chunks(raw_docs)

        # 5. Generación y velocidad de tokens/s
        context_parts = []
        for i, doc in enumerate(docs, 1):
            f_name, p_str = self.extract_doc_source_info(doc)
            context_parts.append(f"[FUENTE {i} | Archivo: {f_name}, {p_str}]:\n{doc.page_content.strip()}")
        context_str = "\n\n".join(context_parts)
        prompt = self._build_prompt(context_str, sample_query)

        t_gen_start = time.perf_counter()
        raw_answer = self.llm.invoke(prompt)
        t_gen_end = time.perf_counter()
        gen_time_s = max(t_gen_end - t_gen_start, 0.001)

        raw_text = raw_answer.content if hasattr(raw_answer, "content") else str(raw_answer)
        tokens_count = self.count_tokens(raw_text)
        gen_speed = round(tokens_count / gen_time_s, 1)

        # 6. Consumo de RAM
        ram_gb = get_process_ram_gb()

        benchmark_result = {
            "indexing_time": indexing_time_str,
            "num_chunks": str(num_chunks),
            "disk_space": format_disk_size(disk_mb),
            "mmr_latency": format_latency(mmr_latency_ms),
            "gen_speed": format_speed(gen_speed),
            "ram_usage": format_ram(ram_gb),
            "raw": {
                "indexing_time_sec": idx_metrics.get("indexing_time_sec") if idx_metrics else None,
                "num_chunks": num_chunks,
                "disk_space_mb": disk_mb,
                "mmr_latency_ms": round(mmr_latency_ms, 1),
                "gen_speed_tok_s": gen_speed,
                "tokens_generated": tokens_count,
                "gen_time_s": round(gen_time_s, 2),
                "ram_usage_gb": ram_gb
            }
        }
        return benchmark_result
