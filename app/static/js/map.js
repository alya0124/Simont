// Inicializa el mapa
var map = L.map('map').setView([0, 0], 2);

// Añade una capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

// Función para obtener la fecha actual en formato YYYY-MM-DD
function fecha_actual() {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Función para obtener los dispositivos del usuario
async function obtenerDispositivos() {
    try {
        const response = await fetch('/get-dispositivos', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al obtener los dispositivos');
        }

        const data = await response.json();
        return data.dispositivos;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

// Función para obtener los datos de la API Flask
async function obtenerDatos(ids) {
    try {
        const fechaFormateada = fecha_actual();
        const params = new URLSearchParams({ ids: ids.join(',') });

        const response = await fetch(`/get-locations/${fechaFormateada}?${params.toString()}`, {
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
    try {
        const dispositivos = await obtenerDispositivos();
        const coordenadas = await obtenerDatos(dispositivos);

        // Eliminar las capas anteriores antes de añadir nuevas
        map.eachLayer(layer => {
            if (layer instanceof L.Polyline) {
                map.removeLayer(layer);
            }
        });

        // Dibujar cada ruta con un color diferente
        const colors = ['blue', 'red', 'green', 'yellow', 'purple', 'orange'];
        let colorIndex = 0;

        dispositivos.forEach(id => {
            const latLngs = coordenadas[id].map(coord => [coord.lat, coord.lng]);
            if (latLngs.length > 0) {
                const polyline = L.polyline(latLngs, { color: colors[colorIndex % colors.length] }).addTo(map);
                colorIndex++;
            }
        });

        // Ajustar el mapa para mostrar todas las rutas
        const allLatLngs = dispositivos.flatMap(id => coordenadas[id].map(coord => [coord.lat, coord.lng]));
        if (allLatLngs.length > 0) {
            map.fitBounds(allLatLngs);
        }
    } catch (error) {
        console.error('Error al dibujar las rutas:', error);
    }
}

// Actualiza el mapa cada 1 segundo
setInterval(dibujarRuta, 1000);
