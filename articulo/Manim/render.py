"""
Script de Renderizado para el Proyecto AcadAId Manim.
Permite compilar fácilmente las escenas con diferentes opciones de calidad y tema.

Uso rápido:
    python render.py                     # Renderiza la escena principal en 1080p
    python render.py --preview           # Renderizado ultra-rápido en 480p para previsualizar
    python render.py --scene slide       # Renderiza la versión limpia de diapositiva
    python render.py --theme dark        # Renderiza en tema oscuro
"""

import argparse
import subprocess
import sys
import os

SCENES = {
    "conceptual": {
        "file": os.path.join("scenes", "scene_01_marco_conceptual.py"),
        "class": "MarcoConceptualScene",
        "desc": "Video explicativo completo del Marco Conceptual (Diapositiva + Diagramas)",
    },
    "slide": {
        "file": os.path.join("scenes", "scene_01_slide_clean.py"),
        "class": "SlideLimpioScene",
        "desc": "Diapositiva animada limpia (idéntica al slide estático con transiciones)",
    },
    "weights3d": {
        "file": os.path.join("scenes", "scene_02_matriz_pesos_3d.py"),
        "class": "MatrizPesos3DScene",
        "desc": "Tensor Cúbico 3D de Pesos de la Red Neuronal (IA en ejecución)",
    },
    "llm3d": {
        "file": os.path.join("scenes", "scene_03_llm_training_3d.py"),
        "class": "LLMTraining3DScene",
        "desc": "Animación 3D del LLM alimentado por palabras y sílabas (Autoatención y Generación)",
    },
    "mmr3d": {
        "file": os.path.join("scenes", "scene_04_mmr_3d.py"),
        "class": "MMR3DScene",
        "desc": "Animación 3D de Relevancia Marginal Máxima (MMR) en Investigación Científica",
    },
}

QUALITY_FLAGS = {
    "preview": "-ql",    # 480p, 15fps (Rápido)
    "medium": "-qm",     # 720p, 30fps
    "high": "-qh",       # 1080p, 60fps (Recomendado para presentaciones)
    "4k": "-qk",         # 2160p, 60fps
}


def probe_manim():
    """
    Detecta de forma inteligente qué intérprete de Python o ejecutable
    puede ejecutar Manim correctamente en este sistema, solucionando problemas
    de entornos virtuales reubicados desde otro disco o usuario.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    site_packages = os.path.join(base_dir, ".venv", "Lib", "site-packages")
    user_profile = os.environ.get("USERPROFILE", "")

    candidates = []

    # 1. Python activo en la terminal
    candidates.append(([sys.executable, "-m", "manim"], f"Python activo ({sys.executable})", {}))
    candidates.append(([sys.executable, "-m", "manim"], f"Python activo con site-packages del .venv", {"PYTHONPATH": site_packages}))

    # 2. Python Launcher de Windows (py.exe)
    candidates.append((["py", "-3.13", "-m", "manim"], "Python Launcher (py -3.13)", {}))
    candidates.append((["py", "-3.13", "-m", "manim"], "Python Launcher (py -3.13) con site-packages", {"PYTHONPATH": site_packages}))
    candidates.append((["py", "-3", "-m", "manim"], "Python Launcher (py -3)", {}))
    candidates.append((["py", "-3", "-m", "manim"], "Python Launcher (py -3) con site-packages", {"PYTHONPATH": site_packages}))
    candidates.append((["py", "-m", "manim"], "Python Launcher (py)", {}))

    # 3. Rutas comunes de Python en Windows
    common_pythons = [
        os.path.join(user_profile, "AppData", "Local", "Programs", "Python", "Python313", "python.exe"),
        os.path.join(user_profile, "AppData", "Local", "Programs", "Python", "Python312", "python.exe"),
        r"C:\Python313\python.exe",
        r"C:\Python312\python.exe",
        r"C:\Program Files\Python313\python.exe",
        r"C:\Program Files\Python312\python.exe",
    ]
    for p in common_pythons:
        if os.path.exists(p):
            candidates.append(([p, "-m", "manim"], f"Python en {p}", {}))
            candidates.append(([p, "-m", "manim"], f"Python en {p} con site-packages", {"PYTHONPATH": site_packages}))

    # 4. Intentar ejecutar manim directamente si está en PATH
    import shutil
    if shutil.which("manim"):
        candidates.append((["manim"], "Comando 'manim' global en PATH", {}))

    # Probar cada candidato
    for cmd_prefix, desc, env_extra in candidates:
        env = os.environ.copy()
        env.update(env_extra)

        test_cmd = cmd_prefix[:-2] + ["-c", "import manim; print('OK')"] if cmd_prefix[-2:] == ["-m", "manim"] else cmd_prefix + ["--version"]
        try:
            res = subprocess.run(test_cmd, capture_output=True, text=True, timeout=5, env=env)
            if res.returncode == 0:
                print(f"[*] Entorno Manim detectado con exito: {desc}")
                return cmd_prefix, env
        except Exception:
            continue

    return None, None


def interactive_selection():
    """
    Menú interactivo en terminal para elegir qué escenas renderizar y en qué calidad.
    """
    print("\n" + "=" * 65)
    print("🎬 SELECCIONADOR DE VIDEOS PARA RENDERIZAR (AcadAId)")
    print("=" * 65)
    scene_keys = list(SCENES.keys())
    for idx, key in enumerate(scene_keys, 1):
        print(f" [{idx}] {key:<12} -> {SCENES[key]['desc']}")
    print(f" [A] all          -> Renderizar TODAS las escenas")
    print("=" * 65)

    sc_input = input("\nElige los videos (ej: '4,5' o 'all' o números separados por espacio): ").strip().lower()
    selected_scenes = []

    if sc_input in ["a", "all", "*"]:
        selected_scenes = scene_keys
    else:
        parts = sc_input.replace(",", " ").split()
        for p in parts:
            if p.isdigit():
                i = int(p) - 1
                if 0 <= i < len(scene_keys):
                    k = scene_keys[i]
                    if k not in selected_scenes:
                        selected_scenes.append(k)
            elif p in SCENES:
                if p not in selected_scenes:
                    selected_scenes.append(p)

    if not selected_scenes:
        print("[!] No seleccionaste ninguna escena válida. Abortando.")
        sys.exit(0)

    print("\nCalidad de renderizado:")
    print(" [1] 4K Ultra HD (2160p, 60fps) - ¡MÁXIMA RESOLUCIÓN!")
    print(" [2] Full HD     (1080p, 60fps) - Recomendado")
    print(" [3] Preview     (480p,  15fps) - Rápido para pruebas")
    q_choice = input("Elige la calidad (1-3, por defecto 1 para 4K): ").strip()

    if q_choice == "2":
        chosen_quality = "high"
    elif q_choice == "3":
        chosen_quality = "preview"
    else:
        chosen_quality = "4k"

    return selected_scenes, chosen_quality


def main():
    parser = argparse.ArgumentParser(description="Renderizador Manim para AcadAId")
    parser.add_argument(
        "--scene",
        nargs="+",
        default=["conceptual"],
        help="Escena(s) a renderizar (ej: --scene mmr3d llm3d, o --scene all)",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Abrir selector interactivo para elegir videos y resolución",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Modo previsualización rápida (-ql, 480p)",
    )
    parser.add_argument(
        "--quality",
        choices=["preview", "medium", "high", "4k"],
        default="high",
        help="Calidad de renderizado (por defecto: high, usa '4k' para máxima resolución)",
    )
    parser.add_argument(
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Tema visual (light por defecto, o dark)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Abrir el reproductor automáticamente tras renderizar",
    )

    args = parser.parse_args()

    # Si se pide modo interactivo, preguntar al usuario
    if args.interactive:
        scenes_to_run, chosen_quality = interactive_selection()
        q_flag = QUALITY_FLAGS[chosen_quality]
    else:
        # Procesar lista de escenas desde CLI
        raw_scenes = []
        for item in args.scene:
            for s in item.replace(",", " ").split():
                raw_scenes.append(s.strip().lower())

        if "all" in raw_scenes:
            scenes_to_run = list(SCENES.keys())
        else:
            scenes_to_run = []
            for s in raw_scenes:
                if s in SCENES:
                    if s not in scenes_to_run:
                        scenes_to_run.append(s)
                else:
                    print(f"\n[!] Error: Escena '{s}' no encontrada.")
                    print(f"    Opciones válidas: {list(SCENES.keys())} o 'all'\n")
                    sys.exit(1)

        q_flag = QUALITY_FLAGS["preview"] if args.preview else QUALITY_FLAGS[args.quality]

    # Actualizar config.py temporalmente si se pide dark mode
    if args.theme == "dark":
        print("[*] Configurando tema oscuro...")
        update_theme_in_config("DARK_THEME")
    else:
        update_theme_in_config("LIGHT_THEME")

    base_cmd, run_env = probe_manim()
    if not base_cmd:
        print("\n" + "=" * 65)
        print("[!] ERROR: No se encontro una instalacion funcional de Manim.")
        print("=" * 65)
        print("El directorio '.venv' contiene binarios configurados para otra ruta")
        print("o usuario anterior ('F:\\Proyectos' y 'C:\\Users\\dduarte').\n")
        print("Solucion recomendada:")
        print("Instala Manim en tu Python actual ejecutando en tu terminal:")
        print(f"    pip install manim")
        print("O regenera el entorno virtual:")
        print("    python -m venv .venv --clear")
        print("    .\\.venv\\Scripts\\pip install manim")
        print("=" * 65 + "\n")
        sys.exit(1)

    for sc_key in scenes_to_run:
        sc_info = SCENES[sc_key]
        print(f"\n=======================================================")
        print(f"[*] Renderizando: {sc_info['desc']}")
        print(f"[*] Archivo: {sc_info['file']} -> {sc_info['class']}")
        print(f"[*] Calidad: {q_flag} | Tema: {args.theme}")
        print(f"[*] Comando: {' '.join(base_cmd)}")
        print(f"=======================================================\n")

        cmd = list(base_cmd) + [q_flag]
        if args.open:
            cmd.append("-p")
        cmd.extend([sc_info["file"], sc_info["class"]])

        try:
            res = subprocess.run(cmd, check=True, env=run_env)
            if res.returncode == 0:
                print(f"\n[OK] Render completado con exito para {sc_key}!")
        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] Error renderizando {sc_key}: {e}", file=sys.stderr)
            sys.exit(1)


def update_theme_in_config(theme_var_name: str):
    config_path = "config.py"
    if not os.path.exists(config_path):
        return
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Reemplazar la línea THEME = ...
    import re
    new_content = re.sub(r"THEME\s*=\s*(LIGHT_THEME|DARK_THEME)", f"THEME = {theme_var_name}", content)
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
