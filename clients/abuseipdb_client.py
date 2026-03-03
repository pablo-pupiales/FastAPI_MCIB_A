

import os
import requests

ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY")
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

def reputacion_ip(ip: str):
    """
    Consulta el score de reputación de una IP en los últimos 90 días.
    Retorna el JSON normalizado de la API si la clave está presente.
    """
    if not ABUSEIPDB_KEY:
        return {"ok": False, "msg": "Falta ABUSEIPDB_KEY en .env", "data": None}

    headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90, "verbose": True}
    r = requests.get(ABUSEIPDB_URL, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    return {"ok": True, "data": r.json().get("data")}