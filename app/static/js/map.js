// Inicializa el mapa
var map = L.map('map', {
    center: [0, 0], // Coordenadas iniciales del centro del mapa
    zoom: 2,       // Nivel de zoom inicial
    scrollWheelZoom: true, // Habilitar zoom con la rueda del mouse
    dragging: true,        // Habilitar arrastre del mapa
    zoomControl: true      // Mostrar controles de zoom
});

// Añade una capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

// Variable para controlar si el mapa debe ajustarse para mostrar todas las rutas
let firstLoad = true;

// Variable para controlar si el mapa está siguiendo un marcador
let followMarker = null;

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

// Función para obtener los datos de los choferes por ID
async function obtenerDatosChoferes(ids) {
    try {
        const params = new URLSearchParams({ ids: ids.join(',') });

        const response = await fetch(`/get-date-choferes?${params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al obtener los datos de los choferes');
        }

        const data = await response.json();
        return data;  // Devuelve los datos de los choferes
    } catch (error) {
        console.error('Error:', error);
        return {};
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

// Mostrar el modal
function showModal(data) {
    var fecha = fecha_actual();
    document.getElementById('choferNombre').textContent = data.nombre || 'No disponible';
    document.getElementById('choferApellidoPaterno').textContent = data.apellido_paterno || 'No disponible';
    document.getElementById('choferApellidoMaterno').textContent = data.apellido_materno || 'No disponible';
    
    if (data.asistencias && data.asistencias[fecha]) {
        document.getElementById('choferAsistencia').textContent = data.asistencias[fecha].asistencia ? 'Sí' : 'No';
        document.getElementById('choferHoraEntrada').textContent = data.asistencias[fecha].hora_registro || 'No disponible';
    } else {
        document.getElementById('choferAsistencia').textContent = 'No disponible';
        document.getElementById('choferHoraEntrada').textContent = 'No disponible';
    }
    
    document.getElementById('choferModal').style.display = 'flex';
}

// Ocultar el modal
function closeModal() {
    document.getElementById('choferModal').style.display = 'none';
}

// Event listener para cerrar el modal
document.getElementById('choferModalClose').addEventListener('click', closeModal);

// Función para dibujar la ruta en el mapa
async function dibujarRuta() {
    try {
        const dispositivos = await obtenerDispositivos();
        const coordenadas = await obtenerDatos(dispositivos);
        const datos_choferes = await obtenerDatosChoferes(dispositivos);
        console.log(datos_choferes);

        // Eliminar las capas anteriores antes de añadir nuevas
        map.eachLayer(layer => {
            if (layer instanceof L.Polyline || layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        // Dibujar cada ruta con un color diferente
        const colors = ['blue', 'red', 'green', 'yellow', 'purple', 'orange'];
        let colorIndex = 0;

        let ultimaCoordenada = null;

        dispositivos.forEach(id => {
            const latLngs = coordenadas[id].map(coord => [coord.lat, coord.lng]);
            if (latLngs.length > 0) {
                const polyline = L.polyline(latLngs, { color: colors[colorIndex % colors.length] }).addTo(map);
                const lastCoord = latLngs[latLngs.length - 1];
                
                // Crear un icono personalizado con el color de la línea
                const iconHtml = `
                    <div class="custom-marker" style="background-color: ${colors[colorIndex % colors.length]}">
                        ${id}
                    </div>
                `;
                const customIcon = L.divIcon({
                    html: iconHtml,
                    className: 'custom-icon',
                    iconSize: [24, 24],
                    iconAnchor: [12, 24]
                });
                
                // Añadir el marcador con popup y evento de click
                const marker = L.marker(lastCoord, { icon: customIcon })
                    .bindPopup(`Dispositivo: ${id}<br>Última posición: (${lastCoord[0]}, ${lastCoord[1]})`)
                    .addTo(map);

                marker.on('click', () => {
                    const choferData = datos_choferes[id];
                    if (choferData) {
                        // Mostrar el modal con los datos del chofer
                        showModal(choferData);
                    } else {
                        console.log('No se encontraron datos del chofer para el ID:', id);
                    }
                });
                
                ultimaCoordenada = lastCoord; // Guardar la última coordenada
                colorIndex++;
            }
        });

        // Ajustar el mapa para mostrar todas las rutas sólo en la primera carga
        if (firstLoad && ultimaCoordenada) {
            map.setView(ultimaCoordenada, 13); // Ajusta el nivel de zoom según sea necesario
            firstLoad = false;
        }
    } catch (error) {
        console.error('Error al dibujar las rutas:', error);
    }
}

// Evento para salir del modo de seguimiento al hacer clic en el mapa
map.on('click', () => {
    followMarker = null;
});

// Función para actualizar el mapa
async function actualizarMapa() {
    await dibujarRuta();
    if (followMarker) {
        map.setView(followMarker.getLatLng(), 13);
    }
}

// Actualiza el mapa cada 1 segundo
setInterval(actualizarMapa, 1000);
