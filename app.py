import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
import streamlit as st

from download_model import download_model, MODELS_DIR, MODEL_FILE
from rag_engine import RAGEngine, VECTOR_DBS_DIR
from metrics_manager import (
    get_process_ram_gb,
    get_system_ram_info,
    get_dir_size_mb,
    format_time_duration,
    format_disk_size,
    format_latency,
    format_speed,
    format_ram,
    load_benchmarks,
    save_benchmarks,
    reset_benchmarks_to_default,
    generate_latex_table,
    generate_markdown_table,
    generate_csv_table,
    generate_html_table,
    PARAM_KEYS
)

RESPUESTAS_DIR = Path(__file__).parent / "respuestas_guardadas"
RESPUESTAS_DIR.mkdir(parents=True, exist_ok=True)


def generate_export_text(content: str, query: str = "", sources: list = None, project_name: str = "") -> str:
    """Genera un archivo de texto plano estructurado con la respuesta, metadatos y citas completas."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "=" * 80,
        "ACADAID - SÍNTESIS Y REPORTE DE INVESTIGACIÓN DOCUMENTAL",
        "=" * 80,
        f"Fecha y hora: {now_str}",
        f"Proyecto: {project_name or 'General'}",
    ]
    if query:
        lines.append(f"Consulta: {query}")
    lines.append("=" * 80)
    lines.append("")
    lines.append("RESPUESTA / SÍNTESIS ACADÉMICA:")
    lines.append("-" * 80)
    lines.append(content.strip())
    lines.append("")
    
    if sources:
        lines.append("=" * 80)
        lines.append("FUENTES Y DOCUMENTOS CONSULTADOS:")
        lines.append("-" * 80)
        for idx, doc in enumerate(sources, 1):
            file_name, page_str = RAGEngine.extract_doc_source_info(doc)
            lines.append(f"[{idx}] Documento: {file_name} ({page_str})")
        lines.append("=" * 80)
        
    return "\n".join(lines)


st.set_page_config(
    page_title="AcadAId - Asistente RAG y Monitoreo de Recursos",
    page_icon="📚",
    layout="wide"
)

# Estilos personalizados de la interfaz
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555;
        margin-bottom: 1.2rem;
    }
    .stChatMessage {
        border-radius: 8px;
    }
    .metric-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 136, 229, 0.08);
        border: 1px solid rgba(30, 136, 229, 0.25);
        color: #0D47A1;
        border-radius: 6px;
        padding: 5px 12px;
        font-size: 0.83rem;
        font-family: 'Segoe UI', system-ui, sans-serif;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .metric-badge-item {
        font-weight: 600;
        color: #1565C0;
    }
    .academic-banner {
        background-color: #f8fafc;
        border-left: 4px solid #1E88E5;
        padding: 10px 16px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-size: 0.92rem;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de la sesión
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None
if "active_collection" not in st.session_state:
    st.session_state.active_collection = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "benchmarks" not in st.session_state:
    st.session_state.benchmarks = load_benchmarks()
if "last_benchmark_result" not in st.session_state:
    st.session_state.last_benchmark_result = None

model_path = MODELS_DIR / MODEL_FILE

# ==========================================
# SIDEBAR: CONFIGURACIÓN Y PROYECTOS
# ==========================================
with st.sidebar:
    st.title("⚙️ Configuración")
    st.subheader("1. Modelo IA Local")
    
    if not model_path.exists():
        st.warning("⚠️ El modelo local no se ha encontrado aún.")
        if st.button("📥 Descargar Modelo Local GGUF (~2.2 GB)"):
            with st.spinner("Descargando modelo desde HuggingFace... Esto puede tardar unos minutos."):
                try:
                    download_model()
                    st.success("¡Modelo descargado correctamente!")
                except Exception as e:
                    st.error(f"Error descargando el modelo: {e}")
    else:
        st.success("✅ Modelo local listo en `./models/`")

    st.divider()
    st.subheader("2. Parámetros del Modelo")
    n_ctx = st.select_slider(
        "🧠 Ventana de Contexto (Tokens)",
        options=[2048, 4096, 8192, 16384],
        value=8192,
        help="Tamaño total de la ventana de contexto del LLM (n_ctx). 8192 tokens es el estándar evaluado en la investigación."
    )
    temperature = st.slider("🌡️ Temperatura (Creatividad)", min_value=0.0, max_value=1.0, value=0.3, step=0.05,
                            help="Valores más bajos hacen que la respuesta sea más precisa y fiel al texto.")
    repeat_penalty = st.slider("🔁 Penalización de Repetición", min_value=1.0, max_value=1.25, value=1.08, step=0.01,
                               help="Rango óptimo: 1.05 a 1.10. Valores superiores a 1.15 provocan colapso del vocabulario.")
    max_tokens = st.slider("📏 Longitud Máxima de Respuesta (Tokens)", min_value=256, max_value=8192, value=1536, step=128,
                           help="Límite máximo de palabras/tokens que puede generar la respuesta (max_tokens). Rango ampliado hasta 8192.")
    k_retriever = st.slider("📑 Fragmentos a consultar (k)", min_value=2, max_value=15, value=8, step=1,
                            help="Cantidad de fragmentos de documentos recuperados. Estándar evaluado k = 8.")

    # Sincronizar parámetros en tiempo real en la sesión activa
    if st.session_state.rag_engine is not None and st.session_state.rag_engine.llm is not None:
        current_n_ctx = getattr(st.session_state.rag_engine, "n_ctx", 8192)
        if current_n_ctx != n_ctx:
            with st.spinner(f"Ajustando ventana de contexto a {n_ctx} tokens en CPU..."):
                st.session_state.rag_engine.init_llm(
                    n_ctx=n_ctx,
                    temperature=temperature,
                    repeat_penalty=repeat_penalty,
                    max_tokens=max_tokens,
                    k_retriever=k_retriever
                )
        elif hasattr(st.session_state.rag_engine, "update_params"):
            st.session_state.rag_engine.update_params(
                temperature=temperature,
                repeat_penalty=repeat_penalty,
                max_tokens=max_tokens,
                k_retriever=k_retriever
            )

    st.divider()
    st.subheader("3. Proyectos / Bases Guardadas")
    
    if VECTOR_DBS_DIR.exists():
        collections = [d.name for d in VECTOR_DBS_DIR.iterdir() if d.is_dir()]
    else:
        collections = []
    
    if collections:
        selected_collection = st.selectbox(
            "📁 Selecciona un proyecto guardado:",
            options=["-- Seleccionar proyecto --"] + collections,
            index=0 if st.session_state.active_collection not in collections else collections.index(st.session_state.active_collection) + 1
        )
        
        if selected_collection != "-- Seleccionar proyecto --" and selected_collection != st.session_state.active_collection:
            with st.spinner(f"Cargando proyecto '{selected_collection}'..."):
                engine = RAGEngine(model_path=str(model_path))
                engine.load_existing_collection(selected_collection)
                engine.init_llm(
                    n_ctx=n_ctx,
                    temperature=temperature,
                    repeat_penalty=repeat_penalty,
                    max_tokens=max_tokens,
                    k_retriever=k_retriever
                )
                st.session_state.rag_engine = engine
                st.session_state.active_collection = selected_collection
                st.session_state.messages = []
                st.success(f"Proyecto '{selected_collection}' cargado.")
                st.rerun()
    else:
        st.info("Aún no tienes proyectos guardados.")

    st.divider()
    st.subheader("4. Crear / Procesar Nuevo Proyecto")
    new_collection_name = st.text_input("🏷️ Nombre del nuevo proyecto:", placeholder="Ej: Articulos_Inteligencia_Artificial")
    
    uploaded_files = st.file_uploader(
        "Sube tus archivos (PDF, DOCX, TXT, MD):",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("🚀 Crear y Procesar Proyecto"):
        if not model_path.exists():
            st.error("Por favor, descarga el modelo local antes de continuar.")
        elif not new_collection_name.strip():
            st.warning("Escribe un nombre para identificar este proyecto o grupo de documentos.")
        else:
            clean_name = new_collection_name.strip().replace(" ", "_")
            with st.spinner("Leyendo, fragmentando e indexando documentos en ChromaDB..."):
                engine = RAGEngine(model_path=str(model_path))
                temp_dir = Path(tempfile.mkdtemp())
                saved_paths = []
                for uf in uploaded_files:
                    file_path = temp_dir / uf.name
                    with open(file_path, "wb") as f:
                        f.write(uf.getvalue())
                    saved_paths.append(str(file_path))

                num_chunks = engine.process_documents(saved_paths, clean_name)
                
                with st.spinner("Inicializando modelo local en CPU..."):
                    engine.init_llm(
                        n_ctx=n_ctx,
                        temperature=temperature,
                        repeat_penalty=repeat_penalty,
                        max_tokens=max_tokens,
                        k_retriever=k_retriever
                    )

                st.session_state.rag_engine = engine
                st.session_state.active_collection = clean_name
                st.session_state.messages = []
                
                idx_meta = engine.last_indexing_metrics
                time_str = idx_meta.get("indexing_time_formatted", "") if idx_meta else ""
                st.success(f"¡Proyecto '{clean_name}' creado con {num_chunks} fragmentos en {time_str}!")
                st.rerun()

    st.divider()
    with st.expander("📁 Respuestas Guardadas en Disco"):
        saved_txts = sorted(list(RESPUESTAS_DIR.glob("*.txt")), key=os.path.getmtime, reverse=True)
        if saved_txts:
            st.caption(f"Total: {len(saved_txts)} archivos guardados en `./respuestas_guardadas/`")
            for sf in saved_txts[:10]:
                st.text(f"📄 {sf.name}")
        else:
            st.caption("Aún no has guardado respuestas en el disco.")

    # Widget inferior de monitoreo de RAM del sistema
    st.divider()
    sys_ram = get_system_ram_info()
    proc_ram = get_process_ram_gb()
    active_ctx = getattr(st.session_state.rag_engine, "n_ctx", n_ctx) if st.session_state.rag_engine else n_ctx
    st.caption(f"🖥️ **RAM Proceso:** {proc_ram} GB | **Sistema:** {sys_ram['used_gb']}/{sys_ram['total_gb']} GB ({sys_ram['percent']}%) | **Ctx:** {active_ctx} tok")


# ==========================================
# ENCABEZADO PRINCIPAL Y PESTAÑAS
# ==========================================
st.markdown('<div class="main-header">📚 AcadAId - Sistema RAG Local para Investigación</div>', unsafe_allow_html=True)
if st.session_state.active_collection:
    st.markdown(f'<div class="sub-header">📂 Proyecto Activo: <b>{st.session_state.active_collection}</b> &nbsp;|&nbsp; Inferencia 100% Offline en CPU</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="sub-header">Investigación documental con rigor metodológico, citas de página garantizadas y cero filtración de datos.</div>', unsafe_allow_html=True)

# Pestañas principales de la aplicación
tab_chat, tab_benchmarks = st.tabs(["💬 Asistente RAG", "📊 Monitoreo y Benchmarking"])


# ==========================================
# PESTAÑA 1: CHAT ASISTENTE RAG
# ==========================================
with tab_chat:
    if not st.session_state.active_collection or st.session_state.rag_engine is None:
        st.info("👈 Para comenzar a consultar, selecciona un proyecto guardado de la barra lateral o crea uno nuevo subiendo tus documentos.")
    else:
        # Mostrar historial de mensajes del chat
        for idx_msg, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Mostrar fuentes consultadas
                if "sources" in message and message["sources"]:
                    with st.expander("📌 Archivos fuentes consultados"):
                        for idx, doc in enumerate(message["sources"], 1):
                            file_name, page_str = RAGEngine.extract_doc_source_info(doc)
                            st.markdown(f"**Fuente {idx}:** `{file_name}` ({page_str})")
                            st.caption(doc.page_content[:300] + "...")
                
                # Mostrar métricas de monitoreo de la respuesta si existen
                if message["role"] == "assistant" and "metrics" in message and message["metrics"]:
                    m = message["metrics"]
                    mmr_val = m.get("mmr_latency_ms", "-")
                    spd_val = m.get("gen_speed_tok_s", "-")
                    tok_val = m.get("tokens_generated", "-")
                    time_val = m.get("gen_time_s", "-")
                    ram_val = m.get("ram_usage_gb", "-")
                    st.markdown(
                        f'<div class="metric-pill">'
                        f'⏱️ Latencia MMR: <span class="metric-badge-item">{mmr_val} ms</span> &nbsp;|&nbsp; '
                        f'⚡ Velocidad: <span class="metric-badge-item">{spd_val} tok/s</span> ({tok_val} tokens en {time_val}s) &nbsp;|&nbsp; '
                        f'💾 RAM: <span class="metric-badge-item">{ram_val} GB</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                # Opciones de exportación para respuestas del asistente
                if message["role"] == "assistant":
                    query_text = message.get("query", "")
                    if not query_text and idx_msg > 0 and st.session_state.messages[idx_msg - 1]["role"] == "user":
                        query_text = st.session_state.messages[idx_msg - 1]["content"]

                    export_text = generate_export_text(
                        content=message["content"],
                        query=query_text,
                        sources=message.get("sources", []),
                        project_name=st.session_state.active_collection or ""
                    )
                    
                    clean_name = (st.session_state.active_collection or "respuesta").strip().replace(" ", "_")
                    filename_txt = f"{clean_name}_resp_{idx_msg}.txt"

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.download_button(
                            label="📥 Descargar respuesta (.txt)",
                            data=export_text,
                            file_name=filename_txt,
                            mime="text/plain; charset=utf-8",
                            key=f"dl_txt_{idx_msg}"
                        )
                    with col2:
                        if st.button("💾 Guardar en carpeta del proyecto", key=f"save_disk_{idx_msg}"):
                            target_file = RESPUESTAS_DIR / filename_txt
                            with open(target_file, "w", encoding="utf-8") as f:
                                f.write(export_text)
                            st.success(f"Guardado en `./respuestas_guardadas/{filename_txt}`")

        # Entrada de texto del chat
        if prompt := st.chat_input("Escribe tu consulta académica (ej: 'Sintetiza la metodología y contrasta los hallazgos empíricos...'):"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                status_container = st.status("🔍 Recuperando fragmentos con algoritmo MMR...", expanded=True)
                try:
                    response_placeholder = st.empty()
                    
                    # Ejecutar la consulta en la cadena de RAG midiendo métricas
                    response_data = st.session_state.rag_engine.ask(prompt)
                    ans = response_data["result"]
                    sources = response_data["source_documents"]
                    metrics = response_data.get("metrics", {})

                    status_container.update(label="✅ Análisis completado con trazabilidad documental", state="complete", expanded=False)
                    
                    response_placeholder.markdown(ans)
                    if sources:
                        with st.expander("📌 Archivos fuentes consultados"):
                            for idx, doc in enumerate(sources, 1):
                                file_name, page_str = RAGEngine.extract_doc_source_info(doc)
                                st.markdown(f"**Fuente {idx}:** `{file_name}` ({page_str})")
                                st.caption(doc.page_content[:300] + "...")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ans,
                        "sources": sources,
                        "query": prompt,
                        "metrics": metrics
                    })
                    st.rerun()
                except Exception as e:
                    status_container.update(label="❌ Ocurrió un error en el procesamiento", state="error", expanded=True)
                    st.error(f"Error al generar la respuesta: {e}")


# ==========================================
# PESTAÑA 2: MONITOREO Y BENCHMARKING
# ==========================================
with tab_benchmarks:
    st.markdown("""
    <div class="academic-banner">
        <b>🔬 Evaluación Empírica de Desempeño en CPU:</b> Monitorea los 6 parámetros técnicos clave del sistema AcadAId 
        (Tiempo de Indexación, Chunks generados, Espacio ChromaDB, Latencia MMR, Velocidad de Tokens y Consumo de RAM). 
        Los resultados se integran directamente con la <b>Tabla IV</b> del artículo de investigación y pueden exportarse a código LaTeX.
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------
    # 1. TARJETAS DE ESTADO EN TIEMPO REAL (KPIs)
    # ------------------------------------------
    st.subheader("1. Estado del Sistema y Proyecto Activo")
    
    live_ram_proc = get_process_ram_gb()
    live_sys = get_system_ram_info()
    
    if st.session_state.rag_engine:
        live_chunks = st.session_state.rag_engine.get_collection_chunks_count()
        live_disk = st.session_state.rag_engine.get_active_disk_size_mb()
        last_m = st.session_state.rag_engine.last_query_metrics or {}
    else:
        live_chunks = 0
        live_disk = 0.0
        last_m = {}

    col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
    with col_kpi1:
        st.metric(
            label="Consumo de RAM (Proceso)",
            value=f"{live_ram_proc} GB",
            delta=f"{live_sys['percent']}% uso sistema",
            delta_color="off",
            help="Memoria RAM residente ocupada por el motor de inferencia LlamaCpp + Embeddings + ChromaDB."
        )
    with col_kpi2:
        st.metric(
            label="Espacio ChromaDB",
            value=f"{live_disk:.1f} MB",
            help="Espacio físico en disco que ocupa la colección activa actual en ./vector_dbs/."
        )
    with col_kpi3:
        st.metric(
            label="Chunks Generados",
            value=f"{live_chunks:,}",
            help="Cantidad total de fragmentos de texto vectorizados en el proyecto activo."
        )
    with col_kpi4:
        mmr_disp = f"{last_m.get('mmr_latency_ms', '-')} ms" if last_m.get('mmr_latency_ms') else "N/D"
        st.metric(
            label="Última Latencia MMR",
            value=mmr_disp,
            help="Tiempo de ejecución del algoritmo Maximal Marginal Relevance con k = 8."
        )
    with col_kpi5:
        spd_disp = f"{last_m.get('gen_speed_tok_s', '-')} tok/s" if last_m.get('gen_speed_tok_s') else "N/D"
        st.metric(
            label="Velocidad Generación",
            value=spd_disp,
            help="Tasa de generación del LLM en tokens por segundo sobre CPU."
        )

    st.divider()

    # ------------------------------------------
    # 2. TABLA COMPARATIVA DE PARÁMETROS EVALUADOS
    # ------------------------------------------
    st.subheader("2. Tabla Comparativa de Rendimiento (Publicación Académica)")
    st.caption("Esta tabla refleja la estructura y métricas empíricas documentadas en el artículo científico (Tabla IV):")
    
    # Renderizar tabla HTML académica tipo booktabs
    html_table = generate_html_table(st.session_state.benchmarks)
    st.markdown(html_table, unsafe_allow_html=True)

    st.divider()

    # ------------------------------------------
    # 3. HERRAMIENTA DE EVALUACIÓN Y BENCHMARKING
    # ------------------------------------------
    st.subheader("3. Ejecutar Evaluación Empírica en Proyecto Activo")
    
    if st.session_state.rag_engine and st.session_state.active_collection:
        st.write(f"Puedes ejecutar un test controlado sobre la colección activa **'{st.session_state.active_collection}'** para calcular sus 6 parámetros y agregarlos como una nueva columna en la tabla comparativa.")
        
        col_b1, col_b2 = st.columns([3, 1])
        with col_b1:
            bench_query = st.text_input(
                "Pregunta de prueba representativa:",
                value="Sintetiza los puntos clave y conceptos principales abordados en los documentos.",
                help="Consulta utilizada para evaluar la latencia de recuperación MMR y la velocidad de generación del LLM."
            )
        with col_b2:
            bench_k = st.number_input("Valor k (retriever):", min_value=2, max_value=15, value=8, step=1)

        if st.button("🧪 Ejecutar Evaluación en Proyecto Activo", type="primary"):
            with st.spinner("Ejecutando prueba de recuperación MMR y generación de tokens en CPU..."):
                try:
                    res = st.session_state.rag_engine.run_benchmark(sample_query=bench_query, k=bench_k)
                    st.session_state.last_benchmark_result = res
                    st.success("¡Evaluación completada con éxito!")
                except Exception as e:
                    st.error(f"Error al ejecutar el benchmark: {e}")

        # Mostrar resultados de la última evaluación si está disponible
        if st.session_state.last_benchmark_result:
            b_res = st.session_state.last_benchmark_result
            st.markdown("##### 📈 Resultados Obtenidos en la Prueba:")
            
            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                st.markdown(f"- **Tiempo de Indexación:** `{b_res['indexing_time']}`")
                st.markdown(f"- **Número de Chunks:** `{b_res['num_chunks']}`")
            with r_col2:
                st.markdown(f"- **Espacio en Disco (ChromaDB):** `{b_res['disk_space']}`")
                st.markdown(f"- **Latencia MMR (k={bench_k}):** `{b_res['mmr_latency']}`")
            with r_col3:
                st.markdown(f"- **Velocidad de Generación:** `{b_res['gen_speed']}`")
                st.markdown(f"- **Consumo de RAM:** `{b_res['ram_usage']}`")

            # Formulario para incorporar a la tabla
            st.markdown("##### ➕ Incorporar a la Tabla Comparativa:")
            col_save1, col_save2, col_save3 = st.columns([2, 2, 1])
            with col_save1:
                col_name_input = st.text_input("Nombre de la columna:", value=st.session_state.active_collection)
            with col_save2:
                col_sub_input = st.text_input("Subtítulo descriptivo:", value=f"({b_res['num_chunks']} chunks, local)")
            with col_save3:
                st.write("")
                st.write("")
                if st.button("💾 Guardar en Tabla"):
                    if col_name_input.strip():
                        name_key = col_name_input.strip()
                        st.session_state.benchmarks[name_key] = {
                            "subtitle": col_sub_input.strip(),
                            "indexing_time": b_res["indexing_time"],
                            "num_chunks": b_res["num_chunks"],
                            "disk_space": b_res["disk_space"],
                            "mmr_latency": b_res["mmr_latency"],
                            "gen_speed": b_res["gen_speed"],
                            "ram_usage": b_res["ram_usage"]
                        }
                        save_benchmarks(st.session_state.benchmarks)
                        st.success(f"Columna '{name_key}' agregada exitosamente a la tabla comparativa.")
                        st.rerun()
    else:
        st.info("👈 Para ejecutar el benchmark en un proyecto real, selecciona o procesa primero un proyecto en la barra lateral.")

    # Expander para gestión de columnas
    with st.expander("⚙️ Gestión y Restauración de Columnas de la Tabla"):
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("**Eliminar una columna existente:**")
            del_options = list(st.session_state.benchmarks.keys())
            col_to_del = st.selectbox("Selecciona la columna a eliminar:", options=del_options)
            if st.button("🗑️ Eliminar Columna Seleccionada"):
                if col_to_del in st.session_state.benchmarks:
                    del st.session_state.benchmarks[col_to_del]
                    save_benchmarks(st.session_state.benchmarks)
                    st.success(f"Columna '{col_to_del}' eliminada.")
                    st.rerun()
        with col_m2:
            st.markdown("**Restaurar valores de referencia originales:**")
            st.caption("Restaura las 3 columnas canónicas del artículo (Pequeño, Medio y Extenso).")
            if st.button("🔄 Restaurar Valores de Referencia del Paper"):
                st.session_state.benchmarks = reset_benchmarks_to_default()
                st.success("Tabla restaurada a los valores de referencia del paper.")
                st.rerun()

    st.divider()

    # ------------------------------------------
    # 4. EXPORTACIÓN DE RESULTADOS PARA PUBLICACIÓN
    # ------------------------------------------
    st.subheader("4. Exportación de Resultados Académicos")
    
    latex_code = generate_latex_table(st.session_state.benchmarks)
    csv_data = generate_csv_table(st.session_state.benchmarks)
    md_table = generate_markdown_table(st.session_state.benchmarks)
    
    exp_col1, exp_col2 = st.columns([1, 1])
    with exp_col1:
        st.download_button(
            label="📄 Descargar Código LaTeX (.tex)",
            data=latex_code,
            file_name="tabla_desempeno_acadaid.tex",
            mime="text/x-tex",
            help="Genera un archivo .tex listo para ser insertado con \\input{} en tu artículo científico."
        )
    with exp_col2:
        st.download_button(
            label="📊 Descargar Datos en CSV (.csv)",
            data=csv_data,
            file_name="metricas_desempeno_acadaid.csv",
            mime="text/csv",
            help="Descarga la matriz de parámetros para importar en Excel o R."
        )

    with st.expander("📋 Ver y Copiar Código LaTeX para `articulo_acadaid.tex`", expanded=False):
        st.code(latex_code, language="latex")

    with st.expander("📝 Ver Tabla en formato Markdown", expanded=False):
        st.markdown(md_table)
