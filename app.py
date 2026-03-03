# app.py
# -----------------------------------------------------------------------------
# Aplicación FastAPI principal.
# endpoints:
#     /api/exposicion        -> datos de Shodan (servicios expuestos en Quito)
#     /api/reputacion/{ip}   -> reputación de IP con AbuseIPDB
#     /api/cves              -> CVEs desde NVD por palabra clave y severidad
# - Carga variables desde archivo .env
# -----------------------------------------------------------------------------



import os
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Cargar variables definidas en .env.
load_dotenv()

# Importar clientes de APIs (módulos locales de la carpeta /clients).
from clients.shodan_client import buscar_exposicion_quito
from clients.abuseipdb_client import reputacion_ip
from clients.nvd_client import buscar_cves
# Opcional: from clients.hibp_client import brechas_por_dominio

app = FastAPI(title="AppCiberseguridadQuito")

# Montar carpeta de estáticos (CSS, JS) y templates (HTML).
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Retorna la plantilla inicial con el mapa y controles.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/exposicion")
def api_exposicion(query: Optional[str] = 'city:"Quito"', limit: int = 50):
    """
    Retorna lista de servicios expuestos con Shodan filtrando por la consulta dada.
    - query: dork de Shodan por defecto con ciudad Quito.
    - limit: cantidad máxima de resultados a devolver.
    """
    try:
        return buscar_exposicion_quito(query=query, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar Shodan: {e}")


@app.get("/api/reputacion/{ip}")
def api_reputacion_ip(ip: str):
    """
    Retorna reputación de una IP consultando AbuseIPDB.
    """
    try:
        return reputacion_ip(ip)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar AbuseIPDB: {e}")


@app.get("/api/cves")
def api_cves(keyword: str = "microsoft", severity: Optional[str] = None, limit: int = 20):
    """
    Retorna CVEs de la NVD por palabra clave y severidad (LOW|MEDIUM|HIGH|CRITICAL).
    """
    try:
        return buscar_cves(keyword=keyword, severity=severity, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar NVD: {e}")
    


