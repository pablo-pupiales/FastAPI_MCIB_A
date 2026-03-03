

import requests

NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def _severity_bucket(score: float):
    """
    Convierte un puntaje CVSS v3 en un texto de severidad aproximado.
    """
    if score is None:
        return None
    if score >= 9.0:
        return "CRITICAL"
    if score >= 7.0:
        return "HIGH"
    if score >= 4.0:
        return "MEDIUM"
    return "LOW"

def buscar_cves(keyword: str = "microsoft", severity: str | None = None, limit: int = 20):
    """
    Busca CVEs por palabra clave y filtra por severidad si se indica.
    Retorna 'count' e 'items' con campos clave (id, description, cvss, severity).
    """
    params = {"keywordSearch": keyword, "resultsPerPage": limit}
    r = requests.get(NVD_API_BASE, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    vulns = []
    for v in data.get("vulnerabilities", []):
        cve = v.get("cve", {})
        metrics = cve.get("metrics") or {}
        v3 = None
        for k in ["cvssMetricV31", "cvssMetricV30"]:
            if k in metrics and metrics[k]:
                v3 = metrics[k][0].get("cvssData")
                break
        score = v3.get("baseScore") if v3 else None
        vulns.append({
            "id": cve.get("id"),
            "published": cve.get("published"),
            "lastModified": cve.get("lastModified"),
            "description": (cve.get("descriptions") or [{}])[0].get("value"),
            "cvss": score,
            "severity": _severity_bucket(score),
        })

    if severity:
        sev = severity.upper()
        vulns = [x for x in vulns if x.get("severity") == sev]

    return {"count": len(vulns), "items": vulns}