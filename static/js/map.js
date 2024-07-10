// Inicializa el mapa
var map = L.map('map').setView([0, 0], 2);

// Añade una capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

// Función para obtener los datos de locations.json
async function obtenerDatos() {
    const response = await fetch('/get-locations');
    if (response.ok) {
        const data = await response.json();
        return data.coordenadas;
    } else {
        const error = await response.json();
        console.error('Error:', error);
        return [];
    }
}

// Función para dibujar la ruta en el mapa
async function dibujarRuta() {
    const coordinates = await obtenerDatos();
    const latLngs = coordinates.map(coord => [coord.lat, coord.lng]);
    const polyline = L.polyline(latLngs, { color: 'blue' }).addTo(map);
    map.fitBounds(polyline.getBounds());
}

// Actualiza el mapa cada 1 segundo
setInterval(dibujarRuta, 1000)