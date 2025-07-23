#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitoreo de Logs en Tiempo Real - Wine IA Web
============================================

Script para monitorear los logs de la aplicación Flask
y proporcionar insights en tiempo real sobre registros y errores.

Uso:
    python monitoring_logs.py

Creado el: 2024-12-30
Autor: Wine IA Development Team
"""

import time
import subprocess
import threading
from datetime import datetime
import sys
import os

class LogMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.log_file = None
        
    def start_monitoring(self):
        """Inicia el monitoreo de logs"""
        print("🔍 Wine IA Log Monitor - INICIADO")
        print("=" * 50)
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📋 Monitoreando eventos de registro y errores...")
        print("💡 Presiona Ctrl+C para detener")
        print("=" * 50)
        
        self.is_monitoring = True
        
        # Mensaje de instrucciones
        print("\n🚀 Para ver logs en acción:")
        print("   1. Ejecuta la aplicación Flask: python app_sommelier.py")
        print("   2. Abre el navegador en http://localhost:5000")
        print("   3. Intenta registrar un usuario")
        print("   4. Los logs aparecerán aquí en tiempo real\n")
        
        # Monitorear consola de Flask
        try:
            while self.is_monitoring:
                time.sleep(1)
                # Aquí podrías implementar lectura de archivos de log
                # Por ahora, solo mostramos el estado de monitoreo
                
        except KeyboardInterrupt:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Detiene el monitoreo de logs"""
        self.is_monitoring = False
        print("\n" + "=" * 50)
        print("🛑 Monitoreo detenido")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

def show_current_users():
    """Muestra los usuarios actuales en la base de datos"""
    print("\n📊 ESTADO ACTUAL DE LA BASE DE DATOS")
    print("=" * 40)
    
    try:
        # Importar módulos necesarios
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from config_sommelier import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consultar usuarios
        cursor.execute("""
            SELECT id, email, first_name, last_name, created_at 
            FROM "User" 
            ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        
        if users:
            print(f"👥 Total de usuarios registrados: {len(users)}")
            print("-" * 40)
            for user in users:
                print(f"🆔 ID: {user[0]}")
                print(f"📧 Email: {user[1]}")
                print(f"👤 Nombre: {user[2]} {user[3]}")
                print(f"📅 Registrado: {user[4]}")
                print("-" * 40)
        else:
            print("❌ No hay usuarios registrados")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al consultar la base de datos: {e}")

def test_registration_flow():
    """Prueba el flujo de registro completo"""
    print("\n🧪 PRUEBA DE FLUJO DE REGISTRO")
    print("=" * 40)
    
    test_data = {
        'firstName': 'Usuario',
        'lastName': 'Prueba',
        'email': f'test_{int(time.time())}@wineai.com',
        'password': 'password123',
        'confirmPassword': 'password123',
        'birthDate': '1990-01-01',
        'newsletter': True,
        'terms': True
    }
    
    print(f"📋 Datos de prueba:")
    for key, value in test_data.items():
        if key not in ['password', 'confirmPassword']:
            print(f"   {key}: {value}")
    
    print("\n💡 Para probar el registro:")
    print("   1. Copia estos datos en el formulario web")
    print("   2. Observa los logs en la consola de Flask")
    print("   3. Verifica que aparezcan los mensajes de logging")

def main():
    """Función principal"""
    print("🍷 Wine IA - Sistema de Monitoreo de Logs")
    print("=========================================\n")
    
    while True:
        print("Selecciona una opción:")
        print("1. 🔍 Iniciar monitoreo en tiempo real")
        print("2. 📊 Mostrar usuarios actuales")
        print("3. 🧪 Mostrar datos de prueba de registro")
        print("4. ❌ Salir")
        
        choice = input("\nOpción (1-4): ").strip()
        
        if choice == '1':
            monitor = LogMonitor()
            monitor.start_monitoring()
        elif choice == '2':
            show_current_users()
        elif choice == '3':
            test_registration_flow()
        elif choice == '4':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida. Intenta de nuevo.")
        
        if choice != '4':
            input("\nPresiona Enter para continuar...")
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
