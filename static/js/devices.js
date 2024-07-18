async function obtenerDispositivos() {
    try {
        const response = await fetch('/get-devices', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error en la respuesta:', errorData);
            throw new Error(errorData.error || 'Error al obtener los dispositivos');
        }

        const data = await response.json();
        console.log('Dispositivos:', data.devices);
        return data.devices;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

// Llama a la función para obtener los dispositivos
obtenerDispositivos().then(devices => {
    // Aquí puedes manejar los dispositivos, por ejemplo, mostrarlos en la interfaz de usuario
    console.log(devices);
});
