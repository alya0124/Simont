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

// Carga los datos de los choferes y dispositivos
function showDeviceTable(deviceId, driverData, color_temp) {
    // Selecciona el cuerpo de la tabla
    var tableBody = document.querySelector('#deviceTable tbody');

    // Crea una nueva fila de datos
    var nuevaFila = tableBody.insertRow();
    nuevaFila.setAttribute('data-id', deviceId);

    // Datos para la fila
    var nombreCompleto = `${driverData.nombre || 'No disponible'} ${driverData.apellido_paterno || 'No disponible'}`;
    
    var colorCell = nuevaFila.insertCell(0);
    var colorSpan = document.createElement('span');
    colorSpan.textContent = '─'; 
    colorSpan.style.color = color_temp; 
    colorCell.appendChild(colorSpan);

    // Añadir celdas de datos
    nuevaFila.insertCell(1).textContent = deviceId || 'No disponible';
    nuevaFila.insertCell(2).textContent = nombreCompleto;

    // Crea la celda de alertas
    var alertasContent = 'No disponible';
    if (driverData.alertas && Object.keys(driverData.alertas).length > 0) {
        alertasContent = '';
        for (var fecha in driverData.alertas) {
            alertasContent += `<strong>${fecha}:</strong> ${driverData.alertas[fecha].join(', ')}<br>`;
        }
    }
    nuevaFila.insertCell(3).innerHTML = alertasContent;

    // Muestra la tabla (asegúrate de que esté visible si estaba oculta)
    document.getElementById('deviceTable').style.display = 'table';
}

function showModal(data) {
    // Actualiza los datos del modal
    document.getElementById('choferNombre').textContent = data.nombre || 'No disponible';
    document.getElementById('choferApellidoPaterno').textContent = data.apellido_paterno || 'No disponible';
    document.getElementById('choferApellidoMaterno').textContent = data.apellido_materno || 'No disponible';
    
    var fecha = fecha_actual();
    if (data.asistencias && data.asistencias[fecha]) {
        document.getElementById('choferAsistencia').textContent = data.asistencias[fecha].asistencia ? 'Sí' : 'No';
        document.getElementById('choferHoraEntrada').textContent = data.asistencias[fecha].hora_registro || 'No disponible';
    } else {
        document.getElementById('choferAsistencia').textContent = 'No disponible';
        document.getElementById('choferHoraEntrada').textContent = 'No disponible';
    }

    document.getElementById('choferModalHeader').style.backgroundColor = '#00332e'
    // Muestra el modal con animación
    var modal = document.getElementById('choferModal');
    modal.style.display = 'flex';
    modal.style.opacity = 0;
    setTimeout(() => modal.style.opacity = 1, 10);
    
}

function closeModal() {
    // Oculta el modal con animación
    var modal = document.getElementById('choferModal');
    modal.style.opacity = 0;
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

// Event listener para cerrar el modal
document.getElementById('choferModalClose').addEventListener('click', closeModal);

// Función para dibujar la ruta en el mapa
async function dibujarRuta() {
    try {
        const dispositivos = await obtenerDispositivos();
        const coordenadas = await obtenerDatos(dispositivos);
        const datos_choferes = await obtenerDatosChoferes(dispositivos);

        // Eliminar las capas anteriores antes de añadir nuevas
        map.eachLayer(layer => {
            if (layer instanceof L.Polyline || layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        // Borra el contenido actual del cuerpo de la tabla
        document.querySelector('#deviceTable tbody').innerHTML = '';

        // Dibujar cada ruta con un color diferente
        const colors = ['blue', 'red', 'green', 'yellow', 'purple', 'orange'];
        let colorIndex = 0;

        let ultimaCoordenada = null;

        dispositivos.forEach(id => {
            const latLngs = coordenadas[id].map(coord => [coord.lat, coord.lng]);
            if (latLngs.length > 0) {

                let color_temp = colors[colorIndex % colors.length];

                const polyline = L.polyline(latLngs, { color: color_temp }).addTo(map);
                const lastCoord = latLngs[latLngs.length - 1];
                
                // Crear un icono personalizado con el color de la línea
                const iconHtml = `
                    <div class="custom-marker" style="background-color: ${color_temp}">
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
                            showModal(choferData);
                        } else {
                            console.log('No se encontraron datos del chofer para el ID:', id);
                        }
                    });
                    

                const choferData = datos_choferes[id];
                showDeviceTable(id, choferData, color_temp)

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
