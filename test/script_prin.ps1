# run_all_scripts.ps1

# Nombres de los scripts
$script1 = "./enviar_coordenadas_random_160.ps1"
$script2 = "./enviar_coordenadas_random_170.ps1"
$script3 = "./enviar_coordenadas_random_180.ps1"

# Ejecutar los scripts
try {
    Write-Output "Ejecutando script enviar_coordenadas_random_160.ps1..."
    . $script1
    Write-Output "Script enviar_coordenadas_random_160.ps1 ejecutado exitosamente."

    Write-Output "Ejecutando script enviar_coordenadas_random_170.ps1..."
    . $script2
    Write-Output "Script enviar_coordenadas_random_170.ps1 ejecutado exitosamente."

    Write-Output "Ejecutando script enviar_coordenadas_random_180.ps1..."
    . $script3
    Write-Output "Script enviar_coordenadas_random_180.ps1 ejecutado exitosamente."
} catch {
    Write-Error "Ocurrió un error: $_"
}

