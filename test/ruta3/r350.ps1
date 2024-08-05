# URL de mi servidor
$flaskUrl = "http://127.0.0.1:443/local"

# Inicializa el índice de la coordenada
$index = 0

# Lista de coordenadas
$lista_coor = @(

@(20.266201488124043, -98.94655551421555),
@(20.266188288370564, -98.94672436418013),
@(20.266175088615967, -98.94709724118525),
@(20.26618168849341, -98.94751936609671),
@(20.266168488738256, -98.94785706602588),
@(20.266392884423183, -98.94794852642336),
@(20.266571080765342, -98.9480540576512),
@(20.266861474365932, -98.9482158722006),
@(20.26740266098957, -98.94848321797787),
@(20.267990044378738, -98.94877870539318),
@(20.26855102639683, -98.94904605117044),
@(20.268907413919425, -98.94925007821098),
@(20.269290199605916, -98.94942596359076),
@(20.269112006386592, -98.94971441561358),
@(20.269006410308194, -98.94994658431487),
@(20.267671380226496, -98.95290525826503),
@(20.266513040131784, -98.95511936143775),
@(20.266313325448387, -98.95690767553879),
@(20.26663286880271, -98.96193198655209),
@(20.26611361049219, -98.9655937725685),
@(20.266033724476717, -98.96742466549054),
@(20.26711218265665, -98.97019229445642),
@(20.267791208055773, -98.97138450376028),
@(20.26886965402034, -98.97206576627497),
@(20.269029423155335, -98.97010713654527),
@(20.269069365413376, -98.96865945370156),
@(20.269069365411926, -98.96780787568072),
@(20.26886965401889, -98.96563635141518),
@(20.268669942368774, -98.96376287949981),
@(20.268510172863603, -98.96027140911207),
@(20.268510172863603, -98.957716674682),
@(20.268190633359673, -98.95477873008744),
@(20.268150690883257, -98.9533310475257),
@(20.268150690883257, -98.95150015451749),
@(20.268789769397547, -98.9506911552813),
@(20.269103403050412, -98.94945190788063),
@(20.268629112164856, -98.94923675939104),
@(20.26824564187824, -98.94908615544833),
@(20.26768052604415, -98.94883873468531),
@(20.26621727012375, -98.947935111029),
@(20.266681879425857, -98.9482236840225),
@(20.266182625852736, -98.94778018312009),
@(20.266210362204493, -98.94727754876405),
@(20.266265834893137, -98.94680448113482)


)


# Índice inicial
$index = 0

# URL del servidor Flask
$flaskUrl = "http://127.0.0.1:443/local"  # Cambia esto a la URL de tu servidor Flask

$fingerprint = "huella_digital_encriptada"

$i = 0

$id = "350"

while ($true) {

     # Obtiene las coordenadas actuales
     $coords = $lista_coor[$index]
     $lat = $coords[0]
     $lon = $coords[1]
 
     # Crea los datos de la solicitud
     if ($i -eq 0) {
        $postData = "id=$id&lat=$lat&lon=$lon&fingerprint=$fingerprint"
    } else {
        $postData = "id=$id&lat=$lat&lon=$lon"
    }
 
     # Envía la solicitud POST usando curl
     $response = curl.exe -X POST -d $postData -H "Content-Type: application/x-www-form-urlencoded" $flaskUrl
 
     # Muestra la respuesta del servidor para depuración
     Write-Output $response
 
     # Incrementa el índice y reinicia si es necesario
     $index = ($index + 1) % $lista_coor.Length
 
     $i++
     # Espera 1 segundo antes de enviar la siguiente solicitud
     Start-Sleep -Seconds 1
}

