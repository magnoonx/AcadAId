import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

BENCHMARKS_FILE = Path(__file__).parent / "benchmarks_data.json"
VECTOR_DBS_DIR = Path(__file__).parent / "vector_dbs"

# Parámetros evaluados estándar según la publicación académica
PARAM_KEYS = [
    ("indexing_time", "Tiempo de Indexación"),
    ("num_chunks", "Número de Chunks generados"),
    ("disk_space", "Espacio en Disco (ChromaDB)"),
    ("mmr_latency", "Latencia de Búsqueda MMR (k = 8)"),
    ("gen_speed", "Velocidad de Generación (tokens/s)"),
    ("ram_usage", "Consumo de RAM (Modelo + DB)")
]

DEFAULT_BENCHMARKS = {
    "Pequeño": {
        "subtitle": "(3 papers, 45 p.)",
        "indexing_time": "12.4 s",
        "num_chunks": "142",
        "disk_space": "1.8 MB",
        "mmr_latency": "45 ms",
        "gen_speed": "8.5 tok/s",
        "ram_usage": "2.6 GB",
        "is_default": True
    },
    "Medio": {
        "subtitle": "(15 papers, 220 p.)",
        "indexing_time": "58.2 s",
        "num_chunks": "710",
        "disk_space": "9.4 MB",
        "mmr_latency": "82 ms",
        "gen_speed": "8.2 tok/s",
        "ram_usage": "2.9 GB",
        "is_default": True
    },
    "Extenso": {
        "subtitle": "(1 libro, 480 p.)",
        "indexing_time": "2 m 14 s",
        "num_chunks": "1650",
        "disk_space": "21.6 MB",
        "mmr_latency": "120 ms",
        "gen_speed": "7.9 tok/s",
        "ram_usage": "3.2 GB",
        "is_default": True
    }
}


def get_process_ram_gb() -> float:
    """Calcula la memoria RAM en GB consumida por el proceso actual y sus subprocesos."""
    if HAS_PSUTIL:
        try:
            proc = psutil.Process(os.getpid())
            mem_bytes = proc.memory_info().rss
            for child in proc.children(recursive=True):
                try:
                    mem_bytes += child.memory_info().rss
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return round(mem_bytes / (1024 ** 3), 2)
        except Exception:
            pass
    return 0.0


def get_system_ram_info() -> Dict[str, Any]:
    """Retorna información general de RAM del sistema."""
    if HAS_PSUTIL:
        try:
            vm = psutil.virtual_memory()
            return {
                "total_gb": round(vm.total / (1024 ** 3), 1),
                "available_gb": round(vm.available / (1024 ** 3), 1),
                "used_gb": round(vm.used / (1024 ** 3), 1),
                "percent": vm.percent
            }
        except Exception:
            pass
    return {"total_gb": 0.0, "available_gb": 0.0, "used_gb": 0.0, "percent": 0.0}


def get_dir_size_mb(directory_path: Path) -> float:
    """Calcula el tamaño total en MB de un directorio en disco."""
    if not directory_path.exists() or not directory_path.is_dir():
        return 0.0
    try:
        total_bytes = sum(f.stat().st_size for f in directory_path.rglob('*') if f.is_file())
        return round(total_bytes / (1024 * 1024), 2)
    except Exception:
        return 0.0


def format_time_duration(seconds: float) -> str:
    """Formatea segundos en notación legible (e.g., '12.4 s' o '2 m 14 s')."""
    if seconds is None:
        return "-"
    if seconds < 60:
        return f"{seconds:.1f} s"
    mins = int(seconds // 60)
    secs = int(round(seconds % 60))
    return f"{mins} m {secs} s"


def format_disk_size(mb: float) -> str:
    if mb is None:
        return "-"
    return f"{mb:.1f} MB"


def format_latency(ms: float) -> str:
    if ms is None:
        return "-"
    return f"{int(round(ms))} ms"


def format_speed(tok_per_sec: float) -> str:
    if tok_per_sec is None:
        return "-"
    return f"{tok_per_sec:.1f} tok/s"


def format_ram(gb: float) -> str:
    if gb is None:
        return "-"
    return f"{gb:.1f} GB"


def load_benchmarks() -> Dict[str, Dict[str, Any]]:
    """Carga el diccionario de benchmarks guardado o los valores por defecto."""
    if BENCHMARKS_FILE.exists():
        try:
            with open(BENCHMARKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and data:
                    return data
        except Exception as e:
            print(f"Aviso al cargar benchmarks_data.json: {e}")
    
    # Si no existe, guardar e inicializar los valores por defecto
    save_benchmarks(DEFAULT_BENCHMARKS)
    return DEFAULT_BENCHMARKS.copy()


def save_benchmarks(data: Dict[str, Dict[str, Any]]) -> None:
    """Guarda los benchmarks actuales en disco."""
    try:
        with open(BENCHMARKS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar benchmarks: {e}")


def reset_benchmarks_to_default() -> Dict[str, Dict[str, Any]]:
    """Restaura los benchmarks a los valores iniciales de la publicación."""
    save_benchmarks(DEFAULT_BENCHMARKS)
    return DEFAULT_BENCHMARKS.copy()


def save_collection_metrics(collection_name: str, metrics: Dict[str, Any]) -> None:
    """Guarda las métricas de indexación dentro de la carpeta de la colección."""
    col_dir = VECTOR_DBS_DIR / collection_name
    if not col_dir.exists():
        return
    meta_file = col_dir / "indexing_metrics.json"
    try:
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando métricas de colección '{collection_name}': {e}")


def load_collection_metrics(collection_name: str) -> Optional[Dict[str, Any]]:
    """Lee las métricas de indexación guardadas de una colección si existen."""
    meta_file = VECTOR_DBS_DIR / collection_name / "indexing_metrics.json"
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def generate_latex_table(benchmarks: Dict[str, Dict[str, Any]]) -> str:
    """Genera el código LaTeX exacto con formato booktabs y tabularx para el paper."""
    cols_keys = list(benchmarks.keys())
    num_cols = len(cols_keys)
    col_align = "c" * num_cols
    
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Métricas de Rendimiento en CPU Doméstica (sin GPU)}",
        r"\label{tab:desempeno}",
        r"\small",
        f"\\begin{{tabularx}}{{\\linewidth}}{{>{{\\raggedright\\arraybackslash}}X {col_align}}}",
        r"\toprule"
    ]
    
    # Fila de nombres de columnas
    header_names = [f"\\textbf{{{name}}}" for name in cols_keys]
    lines.append(r"\textbf{Parámetro Evaluado} & " + " & ".join(header_names) + r" \\")
    
    # Fila de subtítulos (ej: (3 papers, 45 p.))
    header_subtitles = [benchmarks[k].get("subtitle", "") for k in cols_keys]
    lines.append(" & " + " & ".join(header_subtitles) + r" \\")
    lines.append(r"\midrule")
    
    # Filas de métricas
    for key, label in PARAM_KEYS:
        row_vals = []
        for col_name in cols_keys:
            val = benchmarks[col_name].get(key, "-")
            row_vals.append(str(val))
        
        # Ajuste de símbolo matemático en LaTeX para MMR (k=8)
        label_latex = label.replace("(k = 8)", "($k=8$)")
        lines.append(f"{label_latex} & " + " & ".join(row_vals) + r" \\")
        
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabularx}")
    lines.append(r"\end{table}")
    
    return "\n".join(lines)


def generate_markdown_table(benchmarks: Dict[str, Dict[str, Any]]) -> str:
    """Genera la tabla en formato Markdown."""
    cols_keys = list(benchmarks.keys())
    headers = ["**Parámetro Evaluado**"] + [
        f"**{name}**<br><small>{benchmarks[name].get('subtitle', '')}</small>" for name in cols_keys
    ]
    
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]
    
    for key, label in PARAM_KEYS:
        row = [f"**{label}**"] + [str(benchmarks[col_name].get(key, "-")) for col_name in cols_keys]
        lines.append("| " + " | ".join(row) + " |")
        
    return "\n".join(lines)


def generate_csv_table(benchmarks: Dict[str, Dict[str, Any]]) -> str:
    """Genera la tabla en formato CSV descargable."""
    cols_keys = list(benchmarks.keys())
    headers = ['"Parámetro Evaluado"']
    for name in cols_keys:
        sub = benchmarks[name].get("subtitle", "").strip()
        title = f"{name} {sub}".strip() if sub else name
        headers.append(f'"{title}"')
    
    lines = [",".join(headers)]
    for key, label in PARAM_KEYS:
        row = [f'"{label}"'] + [f'"{benchmarks[col].get(key, "-")}"' for col in cols_keys]
        lines.append(",".join(row))
        
    return "\n".join(lines)


def generate_html_table(benchmarks: Dict[str, Dict[str, Any]]) -> str:
    """Genera la tabla con diseño académico tipo booktabs (líneas limpias, tipografía sobria)."""
    cols_keys = list(benchmarks.keys())
    
    html = ['<div style="overflow-x: auto; margin: 1.5rem 0;">']
    html.append('<table style="width: 100%; border-collapse: collapse; font-family: \'Computer Modern\', \'Segoe UI\', sans-serif; font-size: 0.95rem; text-align: center; border-top: 2.2px solid #222; border-bottom: 2.2px solid #222;">')
    
    # Encabezado principal
    html.append('<thead>')
    html.append('<tr style="border-bottom: 1.2px solid #222;">')
    html.append('<th style="text-align: left; padding: 10px 14px; font-weight: 700;">Parámetro Evaluado</th>')
    for col in cols_keys:
        sub = benchmarks[col].get("subtitle", "")
        sub_html = f'<div style="font-weight: 400; font-size: 0.82rem; color: #555; margin-top: 2px;">{sub}</div>' if sub else ''
        html.append(f'<th style="padding: 10px 14px; font-weight: 700;">{col}{sub_html}</th>')
    html.append('</tr>')
    html.append('</thead>')
    
    # Cuerpo
    html.append('<tbody>')
    for idx, (key, label) in enumerate(PARAM_KEYS):
        bg = "background-color: rgba(0, 0, 0, 0.02);" if idx % 2 == 1 else ""
        html.append(f'<tr style="{bg} border-bottom: 1px solid #e0e0e0;">')
        html.append(f'<td style="text-align: left; padding: 9px 14px; font-weight: 500;">{label}</td>')
        for col in cols_keys:
            val = benchmarks[col].get(key, "-")
            html.append(f'<td style="padding: 9px 14px; font-family: monospace, monospace; font-size: 0.93rem;">{val}</td>')
        html.append('</tr>')
    html.append('</tbody>')
    html.append('</table>')
    html.append('</div>')
    
    return "\n".join(html)

