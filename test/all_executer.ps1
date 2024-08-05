# Crear un array para almacenar las tareas
$jobs = @()

# Definir las rutas a los scripts
$scripts = @(
    ".\ruta1\r100.ps1",
    ".\ruta1\r110.ps1",
    ".\ruta1\r120.ps1",
    ".\ruta1\r130.ps1",
    ".\ruta1\r140.ps1",
    ".\ruta1\r150.ps1",
    ".\ruta1\r160.ps1",
    ".\ruta1\r170.ps1",
    ".\ruta1\r180.ps1",
    ".\ruta1\r190.ps1",
    ".\ruta2\r200.ps1",
    ".\ruta2\r210.ps1",
    ".\ruta2\r220.ps1",
    ".\ruta2\r230.ps1",
    ".\ruta2\r240.ps1",
    ".\ruta2\r250.ps1",
    ".\ruta2\r260.ps1",
    ".\ruta2\r270.ps1",
    ".\ruta2\r280.ps1",
    ".\ruta2\r290.ps1",
    ".\ruta3\r300.ps1",
    ".\ruta3\r310.ps1",
    ".\ruta3\r320.ps1",
    ".\ruta3\r330.ps1",
    ".\ruta3\r340.ps1",
    ".\ruta3\r350.ps1",
    ".\ruta3\r360.ps1",
    ".\ruta4\r400.ps1",
    ".\ruta4\r410.ps1"
)

# Ejecutar cada script en paralelo
foreach ($script in $scripts) {
    $jobs += Start-Job -ScriptBlock {
        param($scriptPath)
        & $scriptPath
    } -ArgumentList $script
}

# Esperar a que todos los trabajos terminen
$jobs | Wait-Job | Out-Null

# Opcionalmente, obtener los resultados de los trabajos
$jobs | Receive-Job | Out-Null

