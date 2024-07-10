# Función para generar coordenadas aleatorias dentro de un rango específico
function Get-RandomCoordinate {
    param (
        [double]$minLat = -90.0,
        [double]$maxLat = 90.0,
        [double]$minLon = -180.0,
        [double]$maxLon = 180.0
    )
    $lat = Get-Random -Minimum $minLat -Maximum $maxLat
    $lon = Get-Random -Minimum $minLon -Maximum $maxLon
    return @{lat=$lat; lon=$lon}
}

# URL de tu servidor Flask
$flaskUrl = "http://127.0.0.1:5000/local"

# Loop infinito que se puede detener manualmente
while ($true) {
    # Genera coordenadas aleatorias
    $coords = Get-RandomCoordinate

    # Crea los datos de la solicitud
    $postData = "lat=$($coords.lat)&lon=$($coords.lon)"

    # Envía la solicitud POST usando curl
    curl.exe -X POST -d $postData $flaskUrl

    # Espera 1 segundo antes de enviar la siguiente solicitud
    Start-Sleep -Seconds 1
}
