from pathlib import Path

# Project root
ROOT_DIR = Path(__file__).resolve().parents[2]

# Data directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA = DATA_DIR / "raw"
PROCESSED_DATA = DATA_DIR / "processed"

# Models directory
MODELS_DIR = ROOT_DIR / "models"


