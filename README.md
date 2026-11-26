# Proyecto RAG Local en Python con IA y Streamlit

Este proyecto permite cargar documentos (PDF, DOCX, TXT, MD) y realizar preguntas, solicitudes o pedir resúmenes específicos procesados de manera **100% privada y local** mediante un modelo de lenguaje (LLM) descargado dentro de la carpeta del proyecto.

## 🚀 Arquitectura
- **Modelo LLM Local:** Qwen 2.5 3B Instruct (o Llama 3.2 3B) en formato GGUF mediante `llama-cpp-python`.
- **Embeddings Locales:** `sentence-transformers/all-MiniLM-L6-v2`.
- **Base Vectorial:** `ChromaDB` guardada localmente en `./vector_db/`.
- **Interfaz:** `Streamlit`.

## 🛠️ Requisitos Previos
Tener Python 3.10 - 3.13 instalado.

## 📦 Instalación

1. **Crear entorno virtual e instalar dependencias:**
```bash
python -m venv .venv
# En Windows:
.\.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

2. **Descargar el Modelo Local (.gguf):**
Puedes hacerlo directamente ejecutando:
```bash
python download_model.py
```
O bien desde el botón incluido en el panel lateral de la aplicación Streamlit.

## 💻 Ejecución de la Aplicación

Ejecuta la interfaz web con:
```bash
streamlit run app.py
```
O bien haciendo doble clic en `iniciar.bat`.

Abre tu navegador en la URL indicada (usualmente `http://localhost:8501`), sube tus documentos y ¡empieza a chatear con ellos de forma completamente local!

## 📊 Monitoreo y Benchmarking de Rendimiento
La aplicación incluye una pestaña dedicada a **Monitoreo y Benchmarking** que permite auditar en tiempo real y registrar los 6 parámetros técnicos documentados en publicaciones académicas:
1. **Tiempo de Indexación:** Duración del proceso de extracción, segmentación recursiva e inserción vectorial.
2. **Número de Chunks generados:** Conteo de fragmentos vectorizados.
3. **Espacio en Disco (ChromaDB):** Tamaño físico de la base de datos vectorial en disco.
4. **Latencia de Búsqueda MMR ($k=8$):** Tiempo de recuperación diversificada por Relevancia Marginal Máxima.
5. **Velocidad de Generación (tokens/s):** Rendimiento del LLM cuantizado en CPU.
6. **Consumo de RAM (Modelo + DB):** Memoria residente ocupada por el proceso en ejecución.

Además, permite exportar la tabla comparativa directamente en **LaTeX** (`tabularx` con `booktabs`) y **CSV** para su inclusión en artículos de investigación.
