
# Configuración simplificada para Sommelier Inteligente
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / 'static'

MODEL_FILE = STATIC_DIR / 'wine_model.pkl'
SCALER_FILE = STATIC_DIR / 'wine_scaler.pkl'

def cargar_modelo():
    """Carga el modelo y el scaler desde static"""
    try:
        modelo = joblib.load(MODEL_FILE)
        scaler = joblib.load(SCALER_FILE)
        print(f"✅ Modelo cargado: {MODEL_FILE}")
        print(f"✅ Scaler cargado: {SCALER_FILE}")
        return modelo, scaler
    except Exception as e:
        print(f"❌ Error cargando modelo o scaler: {e}")
        return None, None
