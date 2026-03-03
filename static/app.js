document.addEventListener('DOMContentLoaded', () => {
  // Centro del mapa (Quito aproximado)
  const centerQuito = [-0.220, -78.512];

  // Verificar que Leaflet esté disponible
  if (typeof L === 'undefined') {
    console.error('Leaflet no se cargó. Revisa la etiqueta <script> del CDN en index.html');
    alert('No se pudo cargar el mapa (Leaflet). Revisa la consola del navegador.');
    return;
  }

  const map = L.map('map').setView(centerQuito, 12);

  // Capa base OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap'
  }).addTo(map);

  // Capa para marcadores de exposición (Shodan)
  let exposicionLayer = L.layerGroup().addTo(map);

  // Dibuja marcadores
  function renderExposicion(items) {
    exposicionLayer.clearLayers();
    (items || []).forEach(p => {
      if (p.lat && p.lng) {
        const marker = L.circleMarker([p.lat, p.lng], {
          radius: 6,
          color: '#ef4444',
          fillColor: '#ef4444',
          fillOpacity: 0.75
        }).bindPopup(`
          <b>IP:</b> ${p.ip || '-'}<br/>
          <b>Org:</b> ${p.org || '-'}<br/>
          <b>Puerto:</b> ${p.port || '-'}<br/>
          <b>Producto:</b> ${p.product || '-'}<br/>
          <b>Fecha:</b> ${p.timestamp || '-'}
        `);
        marker.addTo(exposicionLayer);
      }
    });
  }

  // Botón Buscar Exposición
  const btnBuscar = document.getElementById('btnBuscar');
  btnBuscar?.addEventListener('click', async () => {
    try {
      const q = document.getElementById('txtDork').value.trim();
      const params = new URLSearchParams({ query: q, limit: '50' });
      const res = await fetch(`/api/exposicion?${params.toString()}`);
      const data = await res.json();

      if (data.ok) {
        renderExposicion(data.items);
      } else {
        

       console.log("Diag backend /api/exposicion:", data); // <- detalle a consola
        alert(`Respuesta del backend:\n\n${JSON.stringify(data, null, 2)}`);

      }
    } catch (err) {
      console.error(err);
      alert('Error consultando exposición. Revisa la consola del navegador.');
    }
  });

  // Botón Reputación IP
  const btnIP = document.getElementById('btnIP');
  btnIP?.addEventListener('click', async () => {
    try {
      const ip = document.getElementById('txtIP').value.trim();
      if (!ip) return;
      const res = await fetch(`/api/reputacion/${ip}`);
      const data = await res.json();
      document.getElementById('ipOut').textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      console.error(err);
      alert('Error consultando reputación IP. Revisa la consola del navegador.');
    }
  });

  // Botón CVEs
  const btnCVE = document.getElementById('btnCVE');
  btnCVE?.addEventListener('click', async () => {
    try {
      const kw = document.getElementById('txtKW').value.trim() || 'microsoft';
      const sev = document.getElementById('selSev').value;
      const url = `/api/cves?keyword=${encodeURIComponent(kw)}&severity=${encodeURIComponent(sev)}&limit=20`;
      const res = await fetch(url);
      const data = await res.json();
      document.getElementById('cveOut').textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      console.error(err);
      alert('Error consultando CVEs. Revisa la consola del navegador.');
    }
  });

});