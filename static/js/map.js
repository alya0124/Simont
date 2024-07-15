function fecha_actual(){

    // Obtener la fecha del día de hoy
    const hoy = new Date();

    // Obtener el día, mes y año
    const dia = hoy.getDate(); // Retorna el día del mes (1-31)
    const mes = hoy.getMonth() + 1; // Retorna el mes (0-11), por eso se suma 1
    const año = hoy.getFullYear(); // Retorna el año con cuatro dígitos

    // Formatear la fecha como una cadena en formato YYYY-MM-DD
    const fechaFormateada = `${año}-${mes.toString().padStart(2, '0')}-${dia.toString().padStart(2, '0')}`;

    return fechaFormateada;

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
        const response = await fetch(`/get-locations/${fechaFormateada}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Error al obtener las coordenadas');
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