# Guía de Arranque: Entorno Virtual y Aplicación Wine IA

## 1. Activar el entorno virtual

Abre PowerShell y ejecuta:

```powershell
cd "c:\Users\Dell\PyhtonIA\Wine_IA_Production"
.\wine_env\Scripts\Activate.ps1
```

---

## 2. Instalar dependencias (si es la primera vez)

```powershell
pip install -r requirements.txt
```

---

## 3. Arrancar la aplicación principal

```powershell
python app_sommelier.py
```

---

> **Notas:**
>
> - Asegúrate de estar siempre en la carpeta del proyecto antes de activar el entorno.
> - Si usas CMD en vez de PowerShell, ejecuta `wine_env\Scripts\activate.bat`.
> - Si tienes problemas de permisos, ejecuta PowerShell como administrador.
