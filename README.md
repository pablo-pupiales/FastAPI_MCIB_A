
##### EL INFORME DEL PROYECTO SE ENCUENTRA EN \Docs\InformeFastAPI Grupo_11.docx #####

# CiberseguridadQuito

Aplicación FastAPI que visualiza:
- **Exposición de servicios** en Quito (API Shodan; ejemplo `city:"Quito" port:3389`).  
- **Reputación de IP** (API AbuseIPDB).  
- **CVE recientes** (API NVD API 2.0).

## Requisitos
- Python 3.10+  

## Instalación y ejecución (Windows PowerShell)

1) Crear carpeta del proyecto \Ciberseguridad y entrar en ella.

2) Crear entorno virtual en powershell:
python -m venv .venv

3) Activar entorno
.\.venv\Scripts\Activate.ps1

4) Ejecutar comandos
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app:app --port 8080 --log-level debug	//Ejecutar en el servidor de la FastAPI
http://127.0.0.1:8080					///Navegación
