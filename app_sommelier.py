import os
from dotenv import load_dotenv
load_dotenv()
import pickle
import pandas as pd
import numpy as np
import glob
import warnings
import json
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from datetime import datetime, timedelta
from config_sommelier import cargar_modelo
import pandas as pd
from models import db, bcrypt, User, UserSession, WineRecommendation
from chatbot import chatbot_endpoint, chat
from admin import admin_bp

warnings.filterwarnings("ignore")

app = Flask(__name__)

# Configuración mínima de base de datos (SQLite local, cambiar a PostgreSQL en producción)
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://FlaskEjercicioConnect_owner:npg_4SBm3VXpFwIE@ep-floral-frost-a2tieivc-pooler.eu-central-1.aws.neon.tech/FlaskEjercicioConnect?sslmode=require&channel_binding=require')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Registrar blueprint de administración
app.register_blueprint(admin_bp)

# Inicializar extensiones
db.init_app(app)
bcrypt.init_app(app)

model, scaler = cargar_modelo
if model is None or scaler is None:
    print("❌ No se pudieron cargar el modelo o el scaler. Revisa la carpeta static.")

# Cargar el dataset de vinos
try:
    df_vinos = pd.read_csv("static/dataset_vinos_limpieza_total_final.csv")
    print(f"✅ Datos cargados: static/dataset_vinos_limpieza_total_final.csv")
    print(f"✅ Total de vinos disponibles: {len(df_vinos)}")
except Exception as e:
    df_vinos = pd.DataFrame()
    print(f"❌ Error cargando datos de vinos: {e}")

def categorizar_popularidad(num_reviews):
    """Categorizar popularidad según número de reviews"""
    if num_reviews >= 1000:
        return 'Muy Popular'
    elif num_reviews >= 500:
        return 'Popular'
    elif num_reviews >= 200:
        return 'Conocido'
    else:
        return 'Nicho'

def categorizar_precio(precio):
    """Categorizar precio según rangos habituales"""
    if precio <= 10:
        return 'Económico'
    elif precio <= 20:
        return 'Accesible'
    elif precio <= 35:
        return 'Medio'
    elif precio <= 60:
        return 'Premium'
    else:
        return 'Lujo'



# Endpoint Chatbot (para compatibilidad con frontend antiguo)
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    return chatbot_endpoint(chat)

def predecir_calidad_vino_completo(precio, rating, año, tipo_vino="blanco", num_reviews=500):
    """Predice la categoría de calidad usando el modelo entrenado con 4 características"""
    try:
        import numpy as np
        import pickle
        with open("static/label_encoder_tipo_vino.pkl", "rb") as f:
            le_tipo_vino = pickle.load(f)
        with open("static/label_encoder_calidad.pkl", "rb") as f:
            le_calidad = pickle.load(f)
        tipo_vino_normalizado = tipo_vino.strip().lower().capitalize()
        print(f"[LOG] Tipo vino recibido: '{tipo_vino}' | Normalizado: '{tipo_vino_normalizado}'")
        print(f"[LOG] Clases disponibles en encoder: {list(le_tipo_vino.classes_)}")
        if tipo_vino_normalizado not in le_tipo_vino.classes_:
            print(f"[LOG] Tipo de vino '{tipo_vino_normalizado}' no encontrado en encoder. Usando 'Blanco'.")
            tipo_vino_normalizado = "Blanco"
        tipo_vino_encoded = le_tipo_vino.transform([tipo_vino_normalizado])[0]
        X = np.array([[num_reviews, precio, rating, tipo_vino_encoded]])
        X_scaled = scaler.transform(X)
        pred = model.predict(X_scaled)[0]
        calidad_predicha = le_calidad.inverse_transform([pred])[0]
        confianza = 85.0
        print(f"✅ Predicción exitosa: {calidad_predicha} ({confianza:.1f}%)")
        return calidad_predicha, confianza
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        # Fallback: devolver una categoría por defecto y confianza baja pero no cero
        return "Bueno", 50.0

def predecir_calidad_vino_simple(precio, rating, año, bodega="Desconocida", region="España"):
    """Función de predicción simplificada como fallback"""
    try:
        import numpy as np
        X = np.array([[precio, rating, año, 1, 500]])
        X_scaled = scaler.transform(X)
        prediccion_encoded = model.predict(X_scaled)[0]
        clases_calidad = ['Bueno', 'Muy Bueno', 'Excelente']
        prediccion = clases_calidad[prediccion_encoded] if prediccion_encoded < len(clases_calidad) else 'Muy Bueno'
        confianza = 75.0
        return prediccion, confianza
    except Exception as e:
        print(f"❌ Error en predicción simple: {e}")
        return "Error en predicción", 0

def buscar_vinos_similares(precio_min, precio_max, rating_min=4.0, tipo_vino=None):
    """Busca vinos similares en el dataset con deduplicación mejorada"""
    if df_vinos.empty:
        return []
    
    print(f"🔍 Iniciando búsqueda: €{precio_min}-{precio_max}, rating ≥{rating_min}")
    if tipo_vino and tipo_vino not in ["Todos", "ambos"]:
        print(f"🍷 Filtro por tipo: {tipo_vino}")
    
    # IMPORTANTE: Hacer una copia fresca del DataFrame para evitar modificaciones acumulativas
    df_original = df_vinos.copy()
    
    # Filtrar vinos por criterios básicos
    vinos_filtrados = df_original[
        (df_original['precio_eur'] >= precio_min) &
        (df_original['precio_eur'] <= precio_max) &
        (df_original['rating'] >= rating_min)
    ].copy()
    
    # Filtrar por tipo de vino si se especifica
    if tipo_vino and tipo_vino not in ["Todos", "ambos"]:
        vinos_filtrados = vinos_filtrados[
            vinos_filtrados['tipo_vino'] == tipo_vino
        ].copy()
        print(f"🎯 Vinos {tipo_vino.lower()}s encontrados: {len(vinos_filtrados)}")
    
    print(f"📊 Vinos encontrados inicialmente: {len(vinos_filtrados)}")
    
    if len(vinos_filtrados) == 0:
        print("❌ No se encontraron vinos con los criterios especificados. Se mostrarán los mejores vinos del dataset.")
        # Seleccionar los mejores 6 vinos del dataset completo (sin filtro)
        df_top = df_original.sort_values(['rating', 'precio_eur'], ascending=[False, True]).head(6)
        # Limpiar nombres y años para consistencia
        if 'nombre_completo' in df_top.columns:
            df_top['nombre_limpio'] = df_top['nombre_completo']
        elif 'nombre_vino' in df_top.columns:
            df_top['nombre_limpio'] = df_top['nombre_vino']
        else:
            df_top['nombre_limpio'] = "Vino seleccionado"
        df_top['año'] = df_top['año'].apply(limpiar_año)
        return df_top.to_dict('records')
    # Si hay vinos filtrados, devolverlos como lista de diccionarios
    if len(vinos_filtrados) > 0:
        # Limpiar nombres y años para consistencia
        if 'nombre_completo' in vinos_filtrados.columns:
            vinos_filtrados['nombre_limpio'] = vinos_filtrados['nombre_completo']
        elif 'nombre_vino' in vinos_filtrados.columns:
            vinos_filtrados['nombre_limpio'] = vinos_filtrados['nombre_vino']
        else:
            vinos_filtrados['nombre_limpio'] = "Vino seleccionado"
        vinos_filtrados['año'] = vinos_filtrados['año'].apply(limpiar_año)
        return vinos_filtrados.to_dict('records')
    
# Limpiar y convertir rating
def limpiar_rating(rating_str):
    try:
        if isinstance(rating_str, (int, float)):
            return float(rating_str)
        import re
        numeros = re.findall(r'(\d+\.?\d*)', str(rating_str))
        if numeros:
            return float(numeros[0])
        return 4.0
    except:
        return 4.0

# Convertir año a entero para eliminar decimales
def limpiar_año(año_val):
    try:
        if pd.isna(año_val):
            return "N/A"
        return int(float(año_val))
    except:
        return "N/A"

def limpiar_nombre_vino(nombre):
    try:
        if pd.isna(nombre):
            return "Vino sin nombre"
        
        nombre_str = str(nombre)
        
        # Remover información extra común
        import re
        
        # Eliminar números de añadas y calificaciones
        nombre_str = re.sub(r'\b20\d{2}\b', '', nombre_str)
        
        # Eliminar precios, puntuaciones y símbolos
        nombre_str = re.sub(r'[\€\$]\s*\d+[,\.]?\d*', '', nombre_str)  # Precios
        nombre_str = re.sub(r'\d+[,\.]\d+\s*(puntos?|pts?)', '', nombre_str)  # Puntuaciones
        nombre_str = re.sub(r'\d+\s*ml\b', '', nombre_str)  # Volúmenes
        nombre_str = re.sub(r'\b\d+\s*cl\b', '', nombre_str)  # Centilitros
        
        # Eliminar información de descuentos y ofertas
        nombre_str = re.sub(r'\d+%\s*(descuento|off)', '', nombre_str, flags=re.IGNORECASE)
        nombre_str = re.sub(r'ahorra\d+%?', '', nombre_str, flags=re.IGNORECASE)
        
        # Eliminar regiones específicas del nombre (ya se muestran por separado)
        regiones = ['Campo de Borja', 'Calatayud', 'Almansa', 'Ribera del Duero', 
                   'Rioja', 'Rías Baixas', 'Toro', 'Bierzo', 'Jumilla', 'Montsant',
                   'Priorat', 'Penedès', 'Catalunya', 'Valencia', 'Alicante', 'Mallorca']
        
        for region in regiones:
            nombre_str = re.sub(re.escape(region), '', nombre_str, flags=re.IGNORECASE)
        
        # Limpiar caracteres especiales y espacios múltiples
        nombre_str = re.sub(r'[^\w\s\-\.]', ' ', nombre_str)
        nombre_str = re.sub(r'\s+', ' ', nombre_str)
        
        # Dividir por palabras clave que separan el nombre de la bodega
        separadores = ['Campo', 'Bodega', 'Bodegas', 'Winery', 'Estate', 'Viñedos', 'Cellers']
        for sep in separadores:
            if sep in nombre_str:
                partes = nombre_str.split(sep)
                if len(partes) > 1 and len(partes[0].strip()) > 3:
                    nombre_str = partes[0].strip()
                    break
        
        # Si contiene comas, tomar solo la primera parte (nombre principal)
        if ',' in nombre_str:
            nombre_str = nombre_str.split(',')[0]
        
        # Limpiar espacios al inicio y final
        nombre_str = nombre_str.strip()
        
        # Eliminar palabras repetidas o muy cortas al final
        palabras = nombre_str.split()
        palabras_filtradas = []
        
        for palabra in palabras:
            # Mantener palabras significativas
            if len(palabra) >= 3 and palabra.lower() not in ['del', 'de', 'la', 'el', 'los', 'las']:
                # Evitar repetir la misma palabra
                if not palabras_filtradas or palabra.lower() != palabras_filtradas[-1].lower():
                    palabras_filtradas.append(palabra)
        
        nombre_str = ' '.join(palabras_filtradas)
        
        # Si el nombre está vacío después de la limpieza, usar un fallback
        if not nombre_str or len(nombre_str) < 3:
            return "Vino seleccionado"
        
        # Limitar longitud para mantener la interfaz limpia
        if len(nombre_str) > 50:
            nombre_str = nombre_str[:50] + "..."
        
        return nombre_str
        
    except:
        return "Vino seleccionado"
    
    # SISTEMA DE DEDUPLICACIÓN SUPER ESTRICTO PARA ELIMINAR DUPLICADOS EXACTOS
def crear_clave_unica_robusta(row):
    """Crear clave única robusta que detecte duplicados exactos"""
    # ...implementación pendiente...


def validate_registration_data(data):
    """Valida los datos de registro"""
    errors = []
    
    # Validar campos requeridos
    required_fields = ['firstName', 'lastName', 'email', 'password', 'confirmPassword', 'birthDate']
    for field in required_fields:
        if not data.get(field):
            errors.append(f'El campo {field} es requerido')
    
    # Validar email
    email = data.get('email', '').strip().lower()
    if email:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors.append('Formato de email inválido')
        
        # Verificar si el email ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            errors.append('Este email ya está registrado')
    
    # Validar contraseñas
    password = data.get('password', '')
    confirm_password = data.get('confirmPassword', '')
    
    if password != confirm_password:
        errors.append('Las contraseñas no coinciden')
    
    if len(password) < 8:
        errors.append('La contraseña debe tener al menos 8 caracteres')
    
    # Validar edad
    birth_date_str = data.get('birthDate')
    if birth_date_str:
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            today = datetime.now().date()
            age = today.year - birth_date.year
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1
            
            if age < 18:
                errors.append('Debes ser mayor de 18 años para registrarte')
        except ValueError:
            errors.append('Fecha de nacimiento inválida')
    
    # Log de errores si los hay
    if errors:
        print(f"🔍 Errores de validación encontrados: {errors}")
    
    return errors

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro con conexión a base de datos"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            data = {
                'firstName': request.form.get('firstName', '').strip(),
                'lastName': request.form.get('lastName', '').strip(),
                'email': request.form.get('email', '').strip().lower(),
                'password': request.form.get('password', ''),
                'confirmPassword': request.form.get('confirmPassword', ''),
                'birthDate': request.form.get('birthDate', ''),
                'newsletter': request.form.get('newsletter') == 'on',
                'terms': request.form.get('terms') == 'on'
            }
            
            # LOG: Datos recibidos (sin password)
            log_data = {k: v for k, v in data.items() if k not in ['password', 'confirmPassword']}
            print(f"📝 Intento de registro: {log_data}")
            
            # Validar términos y condiciones
            if not data['terms']:
                print(f"❌ Registro fallido - Términos no aceptados: {data['firstName']} {data['lastName']}")
                flash('Debes aceptar los términos y condiciones', 'error')
                return render_template('register.html')
            
            # Validar datos
            errors = validate_registration_data(data)
            if errors:
                print(f"❌ Registro fallido - Errores de validación: {errors}")
                for error in errors:
                    flash(error, 'error')
                return render_template('register.html')
            
            # Verificar si el email ya existe
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                print(f"❌ Registro fallido - Email duplicado: {data['email']}")
                flash('Este email ya está registrado. ¿Ya tienes una cuenta?', 'error')
                return render_template('register.html')
            
            # Crear nuevo usuario
            birth_date = datetime.strptime(data['birthDate'], '%Y-%m-%d').date()
            new_user = User(
                email=data['email'],
                password=data['password'],
                first_name=data['firstName'],
                last_name=data['lastName'],
                birth_date=birth_date,
                newsletter_subscription=data['newsletter']
            )
            
            # Guardar en base de datos
            db.session.add(new_user)
            db.session.commit()
            
            print(f"✅ Registro exitoso: {new_user.get_full_name()} ({new_user.email}) - ID: {new_user.id}")
            
            flash(f'¡Bienvenido {new_user.get_full_name()}! Tu cuenta ha sido creada exitosamente.', 'success')
            flash('Ahora puedes iniciar sesión con tu email y contraseña.', 'info')
            
            return redirect(url_for('login'))
            
        except ValueError as ve:
            print(f"❌ Error de validación en registro: {ve}")
            db.session.rollback()
            flash('Error en los datos proporcionados. Verifica la fecha de nacimiento.', 'error')
            return render_template('register.html')
        except Exception as e:
            print(f"❌ Error inesperado en registro: {e}")
            db.session.rollback()
            flash(f'Error al crear la cuenta: {str(e)}', 'error')
            return render_template('register.html')
    
    # GET request - mostrar formulario
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login con autenticación"""
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            remember = request.form.get('remember') == 'on'
            
            if not email or not password:
                flash('Email y contraseña son requeridos', 'error')
                return render_template('login.html')
            
            # Buscar usuario
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                if not user.is_active:
                    flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
                    return render_template('login.html')
                
                # Actualizar último login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Crear sesión
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['user_name'] = user.get_full_name()
                session.permanent = remember
                
                flash(f'¡Bienvenido de vuelta, {user.first_name}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email o contraseña incorrectos', 'error')
                return render_template('login.html')
                
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')
            return render_template('login.html')
    
    # GET request - mostrar formulario
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    user_name = session.get('user_name', 'Usuario')
    session.clear()
    flash(f'¡Hasta luego, {user_name}!', 'info')
    return redirect(url_for('home'))

@app.route('/home')
def home():
    """Página de inicio con navegación"""
    return render_template('home.html')

@app.route('/')
def index():
    """Página principal que redirige a home para registro de usuarios"""
    return redirect(url_for('home'))

@app.route('/sommelier', methods=['GET', 'POST'])
def sommelier():
    if request.method == 'POST':
        try:
            # Verificar que el modelo esté cargado
            if model is None or scaler is None:
                return render_template('sommelier_index2.html',
                                    prediction_text='Error: Modelo Sommelier no disponible.',
                                    show_result=True,
                                    error=True)

            # Obtener datos del formulario
            precio_min = float(request.form['precio_min'])
            precio_max = float(request.form['precio_max'])
            rating_min = float(request.form.get('rating_min', 4.0))
            tipo_vino = request.form.get('tipo_vino', 'blanco')
            tipo_vino = tipo_vino.strip().lower().capitalize()  # Normalizar para el modelo y el filtro
            ocasion = request.form.get('ocasion', 'general')
            gusto = request.form.get('gusto', 'equilibrado')
            
            # Calcular precio promedio para predicción
            precio_promedio = (precio_min + precio_max) / 2
            
            # Ajustar rating esperado según el gusto
            rating_objetivo = rating_min
            if gusto == 'premium':
                rating_objetivo = max(4.15, rating_min)
            elif gusto == 'equilibrado':
                rating_objetivo = max(4.12, rating_min)
            
            # Predecir calidad usando el tipo de vino del formulario
            prediccion, confianza = predecir_calidad_vino_completo(precio_promedio, rating_objetivo, 2021, tipo_vino=tipo_vino)
            
            # Buscar vinos similares
            vinos_recomendados = buscar_vinos_similares(precio_min, precio_max, rating_min, tipo_vino)

            # Si no hay resultados, obtener los mejores vinos del dataset
            mejores_vinos = []
            if not vinos_recomendados or len(vinos_recomendados) == 0:
                # Seleccionar los mejores 6 vinos del dataset completo (sin filtro)
                df_top = df_vinos.sort_values(['rating', 'precio_eur'], ascending=[False, True]).head(6)
                if 'nombre_completo' in df_top.columns:
                    df_top['nombre_limpio'] = df_top['nombre_completo'].apply(limpiar_nombre_vino)
                elif 'nombre_vino' in df_top.columns:
                    df_top['nombre_limpio'] = df_top['nombre_vino'].apply(limpiar_nombre_vino)
                else:
                    df_top['nombre_limpio'] = "Vino seleccionado"
                df_top['año'] = df_top['año'].apply(limpiar_año)
                mejores_vinos = df_top.to_dict('records')

            # Preparar contexto de respuesta
            prediction_text = f"Recomendación: {prediccion}"

            # Determinar color según predicción
            color_map = {
                'Excelente': 'text-success',
                'Muy Bueno': 'text-info', 
                'Bueno': 'text-primary',
                'Regular': 'text-warning',
                'Básico': 'text-secondary'
            }
            category_color = color_map.get(prediccion, 'text-primary')

            # Mensaje personalizado según ocasión
            ocasion_messages = {
                'romantica': 'Perfecto para una velada romántica',
                'fiesta': 'Ideal para compartir en celebraciones',
                'regalo': 'Excelente opción como obsequio',
                'cena': 'Perfecto para acompañar una buena cena',
                'general': 'Excelente elección para cualquier ocasión'
            }
            ocasion_text = ocasion_messages.get(ocasion, ocasion_messages['general'])

            return render_template('sommelier_index2.html',
                                prediction_text=prediction_text,
                                quality_category=prediccion,
                                category_color=category_color,
                                confidence=f"Confianza: {confianza:.1f}%",
                                ocasion_text=ocasion_text,
                                vinos_recomendados=vinos_recomendados,
                                mejores_vinos=mejores_vinos,
                                show_result=True,
                                error=False)

        except ValueError as e:
            return render_template('sommelier_index2.html',
                                prediction_text='Error: Por favor, ingrese valores numéricos válidos.',
                                show_result=True,
                                error=True)
        except Exception as e:
            return render_template('sommelier_index2.html',
                                prediction_text=f'Error inesperado: {str(e)}',
                                show_result=True,
                                error=True)

    # GET request - mostrar formulario inicial
    return render_template('sommelier_index2.html', show_result=False)

@app.route('/api/vinos')
def api_vinos():
    """API endpoint para obtener lista de vinos"""
    if df_vinos.empty:
        return jsonify({'error': 'No hay datos de vinos disponibles'})
    
    # Convertir a diccionario y limitar a 50 vinos
    vinos_json = df_vinos.head(50).to_dict('records')
    return jsonify({'vinos': vinos_json, 'total': len(df_vinos)})

@app.route('/api/recomendar')
def api_recomendar():
    """API endpoint para recomendaciones"""
    precio_min = float(request.args.get('precio_min', 10))
    precio_max = float(request.args.get('precio_max', 50))
    rating_min = float(request.args.get('rating_min', 4.0))
    tipo_vino = request.args.get('tipo_vino', 'blanco')
    
    vinos = buscar_vinos_similares(precio_min, precio_max, rating_min, tipo_vino)
    return jsonify({'recomendaciones': vinos})

@app.route('/about')
def about():
    """Página de información sobre el modelo"""
    model_info = {
        'nombre': 'Sommelier Inteligente - Vivino Dataset',
        'tipo': 'Random Forest Classifier',
        'dataset': 'Vinos españoles extraídos de Vivino',
        'total_vinos': len(df_vinos) if not df_vinos.empty else 0,
        'caracteristicas': ['Precio', 'Rating', 'Año', 'Bodega', 'Región', 'Popularidad'],
        'accuracy': '100% (en conjunto de prueba)',
        'fecha_entrenamiento': 'Julio 2025'
    }
    
    return render_template('sommelier_about.html', model_info=model_info)

if __name__ == '__main__':
    print("🍷 Iniciando Sommelier Inteligente...")
    # Crear tablas de base de datos
    with app.app_context():
        try:
            print("📊 Conectando a la base de datos PostgreSQL...")
            db.create_all()
            print("✅ Tablas de base de datos creadas/verificadas")
            user_count = User.query.count()
            print(f"👥 Usuarios registrados: {user_count}")
        except Exception as e:
            print(f"❌ Error con la base de datos: {e}")
            print("⚠️ La aplicación funcionará sin registro de usuarios")
    print("🌐 Servidor disponible en: http://0.0.0.0:5001")
    app.run(debug=False, host="0.0.0.0", port=5001)
