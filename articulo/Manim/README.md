# AcadAId: Animaciones Manim para Presentación Científica

Proyecto de animación desarrollado con **Manim Community** para explicar los conceptos del artículo y presentación:
> **"Marco de Inferencia Local con Generación Aumentada por Recuperación para la Investigación Académica" (AcadAId)**

---

## 🎯 Contenido del Proyecto

Este repositorio contiene el código fuente para generar videos y animaciones conceptuales de alta calidad para la presentación:

```
Manim/
│
├── config.py                 # Paleta de colores (Modo Claro y Oscuro), fuentes y estilos
├── render.py                 # Script CLI rápido para renderizar videos fácilmente
├── render.bat                # Acceso rápido interactivo para Windows (doble clic)
├── README.md                 # Documentación completa del proyecto
│
├── components/               # Componentes visuales modulares y reutilizables
│   ├── cards.py              # ConceptCard (flecha azul + título negrita + descripción alineada)
│   ├── documents.py          # AcademicDoc (papers/tesis) y CorpusVault (bóveda cerrada)
│   ├── badges.py             # SlideBanner (sin desbordes), StatusBadge y Escudo de bloqueo
│   └── network.py            # LocalInferenceNode y HermeneuticSynthesis (citas y contexto)
│
└── scenes/                   # Escenas animadas
    ├── scene_01_marco_conceptual.py   # Video explicativo completo con diagramas y conceptos
    ├── scene_01_slide_clean.py        # Diapositiva animada pura (idéntica al slide estático)
    ├── scene_02_matriz_pesos_3d.py     # Tensor Cúbico 3D de Pesos Sinápticos (IA en ejecución)
    ├── scene_03_llm_training_3d.py     # Alimentación 3D por palabras/sílabas, autoatención y generación
    └── scene_04_mmr_3d.py              # Relevancia Marginal Máxima (MMR) en Espacio 3D de Embeddings
```

---

## 📽️ Videos Disponibles

### 1. `MMR3DScene` (Relevancia Marginal Máxima en Investigación Científica) 🌟 *Nueva Animación 3D*
Una experiencia visual 3D cinematográfica con rotaciones orbitales dinámicas que explica cómo el algoritmo MMR (Carbonell & Goldstein, 1998) resuelve la recuperación de información para investigación académica:
- **Espacio Semántico 3D de Embeddings**: Ejes tridimensionales cartesianos (*Metodología*, *Rendimiento*, *Privacidad*) sobre una cuadrícula holográfica iluminada.
- **Consulta Científica Radiante ($Q$)**: Vector focal con pulso expansivo representando la necesidad de investigación (*"Inferencia Local & Privacidad en RAG"*).
- **Selección de Máxima Relevancia ($D_1$)**: Identificación del paper base por máxima proximidad coseno y haz de luz esmeralda.
- **El Dilema de la Redundancia & Rotación 3D Crítica**:
  - La cámara rota y se alinea en el ángulo radial de $D_1$ y $D_{\text{red}}$, revelando al espectador que el paper redundante se encuentra casi superpuesto (colineal), aportando cero novedad científica.
  - MMR penaliza la alta similitud inter-documental ($96\%$) y descarta el duplicado que el k-NN tradicional habría seleccionado por error.
- **Rotación Orbital y Selección por Diversidad ($D_2$)**: La cámara orbita hacia el cuadrante opuesto, destacando la gran distancia angular y la novedad empírica aportada por el paper de cuantización y latencia.
- **Tetraedro 3D de Cobertura Científica ($D_3$)**:
  - Incorporación del pilar de privacidad y soberanía de datos.
  - Se genera un poliedro tridimensional (simplex) con caras bioluminiscentes cian, esmeralda y violeta que encierra el volumen máximo de conocimiento holístico sin redundancia.
- **Órbita 360° Continua y Telemetría HUD**: Rotación cinematográfica completa con desglose de la fórmula matemática en tiempo real y comparativa contra k-NN tradicional.

### 2. `LLMTraining3DScene` (Alimentación 3D del LLM por Palabras y Sílabas) 🔥 *Llamativa*
Una experiencia visual 3D que ilustra el pipeline cognitivo y computacional de un LLM:
- **Flujo de Ingestión BPE**: Sílabas y subpalabras flotantes en cápsulas 3D (`"In-"`, `"-fe-"`, `"-ren-"`, `"-cia"`, `"con-"`, `"-tex-"`, `"-to"`, `"AId"`) con sus identificadores de token (`#1014`, etc.) convergen y son absorbidas por el núcleo 3D.
- **Tensor Transformer 3D**: Voxel core $3 \times 3 \times 3$ con sinapsis bioluminiscentes y contenedor cuántico que reacciona con destellos a cada embedding entrante.
- **Cómputo de Auto-Atención**: Rayos de atención cruzada ($\text{Attn}(\mathbf{Q},\mathbf{K},\mathbf{V})$) interconectan los nodos de pesos emitiendo ondas de optimización.
- **Generación Autorregresiva Token a Token**: Las palabras de salida (`"Respuestas"`, `"ancladas"`, `"al"`, `"contexto"`, `"científico"`) emergen proyectadas al frente con sus probabilidades de predicción Softmax ($P \approx 98\%$).
- **HUD Fijo de Telemetría**: Formulaciones matemáticas de autoatención, ventana de contexto de 8k tokens y métricas de inferencia 100% local.

### 3. `MatrizPesos3DScene` (Tensor Cúbico 3D de la IA)
Una animación 3D cinematográfica que simula en tiempo real la construcción y funcionamiento de la matriz de pesos de una red neuronal:
- **Rotación Orbital Continua**: Da la sensación inmersiva de observar una IA trabajando en un laboratorio de cómputo.
- **Génesis Dimensional**: Muestra cómo los pesos evolucionan de un vector 1D $[w_1, w_2, w_3]$ a una matriz 2D $\mathbf{W}_{ij}$ y finalmente al tensor cúbico tridimensional $\mathcal{W}_{ijk} \in \mathbb{R}^{3 \times 3 \times 3}$.
- **Símbolos Algebraicos Holográficos**: 27 elementos $w_{111}, w_{112}, \dots, w_{333}$ orientados dinámicamente hacia el espectador.
- **Propagación Sináptica**: Ondas de activación $\sigma(\mathbf{W}x + b)$ recorriendo las sinapsis entre capas.
- **Vista Explotada de Capas Ocultas**: Las capas se separan temporalmente en el eje Z para inspeccionar los pesos internos de atención ($w_{222}$).
- **Interfaz HUD de Telemetría**: Indicadores de inferencia offline, parámetros activos y optimización local.

### 4. `MarcoConceptualScene` (Video Explicativo Integral RAG)
Explica la diapositiva en dos zonas sincronizadas:
- **Lado Izquierdo**: Presenta el encabezado (*MARCO CONCEPTUAL*), el título (*Generación Aumentada por Recuperación (RAG)*) y revela sucesivamente los 3 pilares con sus flechas cian.
- **Lado Derecho**: Despliega un modelo animado interactivo para cada concepto:
  1. **Anclaje Empírico**: Bóveda del *Corpus Documental Cerrado* con papers y consultas ancladas.
  2. **Prevención de Extrapolación**: Demuestra cómo el motor *100% Local* bloquea la web abierta y elimina respuestas genéricas o alucinaciones.
  3. **Fidelidad Hermenéutica**: Muestra la síntesis científica grounded con citas directas preservando el contexto del autor original.
  4. **Síntesis Global**: Integra los 3 pilares en el flujo de trabajo holístico de AcadAId.

### 5. `SlideLimpioScene` (Diapositiva Animada para Slides)
Reproduce fielmente la imagen estática pero con transiciones progresivas y proporciones seguras (cero desbordes), ideal para insertar directamente dentro de diapositivas en PowerPoint, Keynote o Beamer.

---

## 🚀 Cómo Renderizar

Puedes usar el script unificado `render.py` o hacer doble clic en `render.bat`:

### 1. Selector Interactivo (Recomendado para elegir videos y resolución):
```bash
python render.py --interactive
# o de forma abreviada:
python render.py -i
```
Te mostrará un menú interactivo en terminal para seleccionar uno o varios videos (ej: `4, 5` o `all`) y elegir si los quieres en **4K Ultra HD**, **1080p** o **Preview**.

---

### 2. Renderizar a Máxima Resolución (4K Ultra HD - 2160p 60fps):
Para renderizar videos específicos en **calidad máxima (4K)**, usa el flag `--quality 4k`:

- **Solo MMR 3D en 4K**:
  ```bash
  python render.py --scene mmr3d --quality 4k
  ```
- **Solo LLM 3D en 4K**:
  ```bash
  python render.py --scene llm3d --quality 4k
  ```
- **Varios videos seleccionados en 4K** (ej: MMR 3D + LLM 3D):
  ```bash
  python render.py --scene mmr3d llm3d --quality 4k
  ```
- **TODOS los videos del proyecto en 4K**:
  ```bash
  python render.py --scene all --quality 4k
  ```

---

### 3. Renderizar en Full HD (1080p 60fps - Estándar para Presentaciones):
- **MMR 3D**:
  ```bash
  python render.py --scene mmr3d --quality high
  ```
- **LLM 3D**:
  ```bash
  python render.py --scene llm3d --quality high
  ```
- **Matriz de Pesos 3D**:
  ```bash
  python render.py --scene weights3d --quality high
  ```
- **Marco Conceptual**:
  ```bash
  python render.py --scene conceptual --quality high
  ```
- **Diapositiva Limpia**:
  ```bash
  python render.py --scene slide --quality high
  ```

---

### 4. Previsualización Rápida (480p, ultra rápido para probar cambios):
```bash
python render.py --scene mmr3d --preview
```

---

## 📦 Dónde se guardan los videos generados

Manim almacena los videos renderizados organizados por resolución:
- **Videos 4K Ultra HD (2160p)**:
  `media/videos/<nombre_escena>/2160p60/<NombreClase>.mp4`
- **Videos Full HD (1080p)**:
  `media/videos/<nombre_escena>/1080p60/<NombreClase>.mp4`
- **Previsualizaciones (480p)**:
  `media/videos/<nombre_escena>/480p15/<NombreClase>.mp4`
