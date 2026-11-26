import os
from pathlib import Path
from huggingface_hub import hf_hub_download

MODELS_DIR = Path(__file__).parent / "models"
MODEL_REPO = "Qwen/Qwen2.5-3B-Instruct-GGUF"
MODEL_FILE = "qwen2.5-3b-instruct-q4_k_m.gguf"

def download_model(models_dir=MODELS_DIR, repo_id=MODEL_REPO, filename=MODEL_FILE):
    """
    Descarga el modelo GGUF desde HuggingFace y lo guarda dentro del directorio de modelos del proyecto.
    """
    models_dir.mkdir(parents=True, exist_ok=True)
    destination_path = models_dir / filename

    if destination_path.exists():
        print(f"El modelo ya existe en: {destination_path}")
        return str(destination_path)

    print(f"Descargando modelo {filename} desde HuggingFace ({repo_id})...")
    file_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=models_dir,
        local_dir_use_symlinks=False
    )
    print(f"Modelo descargado con éxito en: {file_path}")
    return file_path

if __name__ == "__main__":
    download_model()
