function fecha_actual() {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}


// Inicializa el mapa
var map = L.map('map').setView([0, 0], 2);

// Añade una capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

// Función para obtener los datos de la API Flask
async function obtenerDatos() {
    try {
        const fechaFormateada = fecha_actual();
        const id = 160;
        const response = await fetch(`/get-locations/${fechaFormateada}/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al obtener las coordenadas');
        }

        const data = await response.json();
        return data.coordenadas;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }

}

// Función para dibujar la ruta en el mapa
async function dibujarRuta() {
    const coordinates = await obtenerDatos();
    const latLngs = coordinates.map(coord => [coord.lat, coord.lng]);
    
    // Eliminar la capa anterior antes de añadir una nueva
    map.eachLayer(layer => {
        if (layer instanceof L.Polyline) {
            map.removeLayer(layer);
        }
    });

    const polyline = L.polyline(latLngs, { color: 'blue' }).addTo(map);
    map.fitBounds(polyline.getBounds());
}

// Actualiza el mapa cada 1 segundo
setInterval(dibujarRuta, 1000);