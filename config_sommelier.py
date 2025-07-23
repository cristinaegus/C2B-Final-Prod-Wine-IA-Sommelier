# Configuración del Sommelier Inteligente
import os
import pickle
from pathlib import Path

class Config:

    @classmethod
    def verificar_archivos_requeridos(cls):
        """Verifica que todos los archivos necesarios existan"""
        archivos_faltantes = []
        # Verificar CSV de datos
        if not cls.LATEST_CSV or not cls.LATEST_CSV.exists():
            archivos_faltantes.append(f"CSV de datos (patrón: {cls.CSV_PATTERN_1} o {cls.CSV_PATTERN_2})")
        # Verificar archivos del modelo
        archivos_modelo = [
            (cls.MODEL_FILE, "Modelo Random Forest"),
            (cls.SCALER_FILE, "Scaler"),
            (cls.ENCODER_FILE, "Label Encoder")
        ]
        for archivo, nombre in archivos_modelo:
            if not archivo.exists():
                archivos_faltantes.append(f"{nombre} ({archivo.name})")
        return archivos_faltantes

    @classmethod
    def cargar_modelo(cls):
        """Carga el modelo y sus componentes"""
        try:
            import joblib
            # Cargar modelo principal
            modelo = joblib.load(cls.MODEL_FILE)
            # Cargar scaler
            scaler = joblib.load(cls.SCALER_FILE)
            # Cargar información del modelo si está disponible
            model_info = None
            if cls.MODEL_INFO_FILE and cls.MODEL_INFO_FILE.exists():
                try:
                    model_info = joblib.load(cls.MODEL_INFO_FILE)
                except:
                    model_info = None
            # Cargar encoder si existe (compatibilidad con modelos antiguos)
            encoder = None
            if cls.ENCODER_FILE.exists():
                try:
                    with open(cls.ENCODER_FILE, 'rb') as f:
                        encoder = pickle.load(f)
                except:
                    encoder = None
            print(f"✅ Modelo cargado exitosamente desde {cls.MODEL_FILE}")
            if model_info:
                print(f"📊 Versión del modelo: {model_info.get('version', 'desconocida')}")
                print(f"📅 Timestamp: {model_info.get('timestamp', 'desconocido')}")
                print(f"🏷️ Clases disponibles: {model_info.get('clases_calidad', [])}")
            return modelo, scaler, encoder, model_info
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return None, None, None, None

    @classmethod
    def obtener_info_dataset(cls):
        """Obtiene información sobre el dataset actual"""
        if not cls.LATEST_CSV:
            return None
        import pandas as pd
        try:
            df = pd.read_csv(cls.LATEST_CSV)
            return {
                'archivo': cls.LATEST_CSV.name,
                'total_vinos': len(df),
                'precio_min': df['precio_euros'].min(),
                'precio_max': df['precio_euros'].max(),
                'rating_min': df['rating'].min(),
                'rating_max': df['rating'].max(),
                'columnas': list(df.columns)
            }
        except Exception:
            return None
    """Configuración centralizada para el Sommelier Inteligente"""
    
    # Rutas del proyecto
    BASE_DIR = Path(__file__).parent
    STATIC_DIR = BASE_DIR / 'static'
    TEMPLATES_DIR = BASE_DIR / 'templates'
    DATA_DIR = BASE_DIR / 'datos_scraping'
    MODELS_DIR = BASE_DIR / 'modelos generados'
    
    # Configuración Flask
    SECRET_KEY = 'sommelier-wine-recommendation-2025'
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5001
    
    # Configuración de la base de datos PostgreSQL Neon
    DATABASE_URL = 'postgresql://FlaskEjercicioConnect_owner:npg_4SBm3VXpFwIE@ep-floral-frost-a2tieivc-pooler.eu-central-1.aws.neon.tech/FlaskEjercicioConnect?sslmode=require&channel_binding=require'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Archivos de datos
    CSV_PATTERN_1 = 'vivino_scraping_completo_*.csv'
    CSV_PATTERN_2 = 'resumen_scraping_completo_*.csv'
    CSV_PATTERN_LIMPIO = 'resumen_scraping_completo_*_limpio_*.csv'  # Archivos limpios prioritarios
    CSV_PATTERN_ULTRA_LIMPIO = 'resumen_scraping_completo_*_ultra_limpio.csv'  # Archivos ultra limpios
    CSV_PATTERN_COMBINADO = 'dataset_vinos_combinado_ultra_limpio_*.csv'  # Dataset balanceado tintos+blancos
    

# Acceso correcto a rutas y archivos usando Config
CSV_FILES_1 = list(Config.DATA_DIR.glob(Config.CSV_PATTERN_1)) if Config.DATA_DIR.exists() else []
CSV_FILES_2 = list(Config.DATA_DIR.glob(Config.CSV_PATTERN_2)) if Config.DATA_DIR.exists() else []
CSV_FILES_LIMPIO = list(Config.DATA_DIR.glob(Config.CSV_PATTERN_LIMPIO)) if Config.DATA_DIR.exists() else []
CSV_FILES_ULTRA_LIMPIO = list(Config.DATA_DIR.glob(Config.CSV_PATTERN_ULTRA_LIMPIO)) if Config.DATA_DIR.exists() else []
CSV_FILES_COMBINADO = list(Config.DATA_DIR.glob(Config.CSV_PATTERN_COMBINADO)) if Config.DATA_DIR.exists() else []

if CSV_FILES_COMBINADO:
    LATEST_CSV = max(CSV_FILES_COMBINADO, key=os.path.getctime)
    print(f"⚖️ Usando dataset BALANCEADO (tintos + blancos): {LATEST_CSV.name}")
elif CSV_FILES_ULTRA_LIMPIO:
    LATEST_CSV = max(CSV_FILES_ULTRA_LIMPIO, key=os.path.getctime)
    print(f"🌟 Usando archivo de datos ULTRA LIMPIO: {LATEST_CSV.name}")
elif CSV_FILES_LIMPIO:
    LATEST_CSV = max(CSV_FILES_LIMPIO, key=os.path.getctime)
    print(f"✨ Usando archivo de datos LIMPIO: {LATEST_CSV.name}")
else:
    CSV_FILES = CSV_FILES_1 + CSV_FILES_2
    LATEST_CSV = max(CSV_FILES, key=os.path.getctime) if CSV_FILES else None
    if LATEST_CSV:
        print(f"📊 Usando archivo de datos original: {LATEST_CSV.name}")

# Definir archivos de modelo usando Config
MODEL_FILE = Config.STATIC_DIR / 'wine_model.pkl' if (Config.STATIC_DIR / 'wine_model.pkl').exists() else (Config.BASE_DIR / 'modelo_random_forest_vivino.pkl' if (Config.BASE_DIR / 'modelo_random_forest_vivino.pkl').exists() else Config.MODELS_DIR / 'modelo_random_forest_vivino.pkl')
SCALER_FILE = Config.STATIC_DIR / 'wine_scaler.pkl' if (Config.STATIC_DIR / 'wine_scaler.pkl').exists() else (Config.BASE_DIR / 'scaler_vivino.pkl' if (Config.BASE_DIR / 'scaler_vivino.pkl').exists() else Config.MODELS_DIR / 'scaler_vivino.pkl')
MODEL_INFO_FILE = Config.STATIC_DIR / 'model_info.pkl' if (Config.STATIC_DIR / 'model_info.pkl').exists() else None
ENCODER_FILE = Config.BASE_DIR / 'label_encoder_vivino.pkl' if (Config.BASE_DIR / 'label_encoder_vivino.pkl').exists() else Config.MODELS_DIR / 'label_encoder_vivino.pkl'

# Asignar estos archivos a la clase Config para mantener compatibilidad
Config.CSV_FILES_1 = CSV_FILES_1
Config.CSV_FILES_2 = CSV_FILES_2
Config.CSV_FILES_LIMPIO = CSV_FILES_LIMPIO
Config.CSV_FILES_ULTRA_LIMPIO = CSV_FILES_ULTRA_LIMPIO
Config.CSV_FILES_COMBINADO = CSV_FILES_COMBINADO
Config.LATEST_CSV = LATEST_CSV
Config.MODEL_FILE = MODEL_FILE
Config.SCALER_FILE = SCALER_FILE
Config.MODEL_INFO_FILE = MODEL_INFO_FILE
Config.ENCODER_FILE = ENCODER_FILE
    
    
    

# Configuración de recomendaciones
Config.DEFAULT_RECOMMENDATIONS = 6
Config.MAX_RECOMMENDATIONS = 12
Config.MIN_RATING = 3.8
Config.MAX_RATING = 5.0
Config.MIN_PRICE = 8.0
Config.MAX_PRICE = 100.0

# Categorías de ocasiones
Config.OCASIONES = {
    'general': 'Uso general',
    'romantica': 'Cena romántica',
    'fiesta': 'Fiesta o celebración',
    'regalo': 'Para regalar',
    'especial': 'Ocasión especial'
}

# Preferencias de gusto
Config.GUSTOS = {
    'equilibrado': 'Equilibrado',
    'premium': 'Premium',
    'economico': 'Económico',
    'popular': 'Popular'
}

# Pesos para el algoritmo de recomendación
Config.FEATURE_WEIGHTS = {
    'rating': 0.35,
    'num_reviews': 0.20,
    'posicion': 0.15,
    'precio': 0.10,
    'popularidad': 0.10,
    'valor': 0.10
}


# Configuración específica para desarrollo

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    HOST = '0.0.0.0'

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

# Selección de configuración basada en variable de entorno
config_mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config(env='development'):
    """Obtiene la configuración según el entorno"""
    return config_mapping.get(env, DevelopmentConfig)
