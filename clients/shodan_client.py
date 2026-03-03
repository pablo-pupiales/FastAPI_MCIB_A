
# Comportamiento:
# - Consulta a Shodan /shodan/host/search con API key.
# - Si Shodan devuelve 403/401/429 u otro HTTP != 200,
#   retorna un conjunto DEMO de puntos para fines didácticos.
# - De este modo el front siempre podrá mostrar marcadores.
# ------------------------------------------------------------

import os
import requests

SHODAN_SEARCH_URL = "https://api.shodan.io/shodan/host/search"

# Dataset mínimo de ejemplo para visualizar en el mapa de Quito.
DEMO_ITEMS = [
    {"ip":"200.24.212.73","org":"Demo Org A","port":3389,"product":"RDP","lat":-0.191,"lng":-78.507,"timestamp":"2026-02-27T10:00:00Z"},
    {"ip":"181.188.193.137","org":"Demo Org B","port":22,"product":"OpenSSH","lat":-0.245,"lng":-78.532,"timestamp":"2026-02-27T10:05:00Z"},
    {"ip":"200.24.213.45","org":"Demo Org C","port":443,"product":"nginx","lat":-0.214,"lng":-78.497,"timestamp":"2026-02-27T10:10:00Z"},
    {"ip":"181.188.197.125","org":"Demo Org D","port":80,"product":"Apache","lat":-0.263,"lng":-78.559,"timestamp":"2026-02-27T10:12:00Z"},
    {"ip":"200.24.212.153","org":"Demo Org E","port":21,"product":"FTP","lat":-0.228,"lng":-78.521,"timestamp":"2026-02-27T10:15:00Z"}
]

def buscar_exposicion_quito(query: str = 'city:"Quito"', limit: int = 50):
    """
    Retorna:
      - ok=True + items (si Shodan responde 200)
      - ok=True + DEMO_ITEMS (si Shodan rechaza, p.ej. 403/401/429)
      - ok=False (solo si hay un error de red)
    """
    shodan_key = os.getenv("SHODAN_API_KEY")

    # Si no hay key, ir directamente a demo (didáctico).
    if not shodan_key:
        return {"ok": True, "count": len(DEMO_ITEMS), "items": DEMO_ITEMS, "demo": True}

    try:
        params = {"key": shodan_key, "query": query}
        r = requests.get(SHODAN_SEARCH_URL, params=params, timeout=30)

        if not r.ok:
            # Log de diagnóstico en servidor
            print(f"[SHODAN][HTTP {r.status_code}] {r.text[:1000]}")

            # Si es 401/403/429 (key inválida, plan insuficiente o rate limit), ir a demo.
            if r.status_code in (401, 403, 429):
                return {"ok": True, "count": len(DEMO_ITEMS), "items": DEMO_ITEMS, "demo": True}

            # Para otros errores HTTP inusuales, también se puede retornar demo:
            return {"ok": True, "count": len(DEMO_ITEMS), "items": DEMO_ITEMS, "demo": True}

        # Caso exitoso con Shodan
        data = r.json()
        items = []
        for m in data.get("matches", []):
            loc = m.get("location") or {}
            product = m.get("product") or (m.get("http") or {}).get("server")
            items.append({
                "ip": m.get("ip_str"),
                "org": m.get("org"),
                "port": m.get("port"),
                "product": product,
                "lat": loc.get("latitude"),
                "lng": loc.get("longitude"),
                "timestamp": m.get("timestamp"),
            })
            if len(items) >= limit:
                break

        return {"ok": True, "count": len(items), "items": items, "demo": False}

    except requests.exceptions.RequestException as e:
        # Error de red: como es didáctico, retornar demo para no bloquear la práctica.
        print(f"[SHODAN][NetworkError] {e}")
        return {"ok": True, "count": len(DEMO_ITEMS), "items": DEMO_ITEMS, "demo": True}