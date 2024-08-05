# URL de mi servidor
$flaskUrl = "http://127.0.0.1:443/local"

# Inicializa el índice de la coordenada
$index = 0

# Lista de coordenadas
$lista_coor = @(

    @(20.266207275528107, -98.946572902822),
    @(20.26620422493421, -98.94658591045655),
    @(20.266219477903082, -98.94670948298491),
    @(20.26620422493421, -98.94687207841696),
    @(20.26620422493421, -98.9470574372095),
    @(20.26616761780278, -98.94770456702902),
    @(20.266356184490295, -98.94798014215377),
    @(20.2672294482347, -98.9484836454741),
    @(20.26736675340776, -98.94849535485363),
    @(20.267498566259597, -98.94865343147748),
    @(20.267674316554515, -98.94870026899564),
    @(20.26815762883907, -98.94891103782741),
    @(20.268498143408287, -98.9490983879001),
    @(20.268740017644536, -98.9491453047442),
    @(20.269026510733536, -98.9492489241643),
    @(20.269277191752437, -98.94941798742863),
    @(20.26915440926318, -98.94964158722988),
    @(20.269067438274494, -98.94983246510895),
    @(20.269067438274494, -98.94982701145527),
    @(20.268806525015926, -98.9504323670147),
    @(20.2686274666434, -98.95075958623603),
    @(20.268448408048876, -98.95113043459823),
    @(20.267967506842062, -98.95212299956955),
    @(20.267895883130542, -98.95223207264333),
    @(20.267808911436386, -98.952482940713),
    @(20.267665663833863, -98.95277743801218),
    @(20.26767589580986, -98.95273380878265),
    @(20.267440560191265, -98.95324099857571),
    @(20.267194992208697, -98.95368819817817),
    @(20.266785035571957, -98.95459608667846),
    @(20.26646853004197, -98.95517512648553),
    @(20.26637015657005, -98.95536661996503),
    @(20.266156300981184, -98.95578152250395),
    @(20.266181963652688, -98.9557906411853),
    @(20.265959553564382, -98.95622378119847),
    @(20.265617383575297, -98.9569760770108),
    @(20.26553611809202, -98.95713565491037),
    @(20.2653222613537, -98.95750496376371),
    @(20.265410901201584, -98.95731978673462),
    @(20.26529012473455, -98.95754509229751),
    @(20.265119024578663, -98.95796351691428),
    @(20.264897600567462, -98.95832829734942),
    @(20.264941994096265, -98.9582323228532),
    @(20.26465514896681, -98.95888141745104),
    @(20.26447901572984, -98.95929447764965),
    @(20.26420726691494, -98.95981482621154),
    @(20.264167007790782, -98.95990065690215),
    @(20.26404119796047, -98.96022788641014),
    @(20.26385499922443, -98.96060876009977),
    @(20.2638399020027, -98.96064631098623),
    @(20.263749318744225, -98.96090916747626),
    @(20.263608411348176, -98.96126858349324),
    @(20.263623508575296, -98.96131149883854),
    @(20.263532925190518, -98.9615689909104),
    @(20.26353795760217, -98.96172455903715),
    @(20.263507763129823, -98.96198741552719),
    @(20.263482601065014, -98.96236292479865),
    @(20.26345240658188, -98.96250239967091),
    @(20.263442341752874, -98.9628457224334),
    @(20.263422212080002, -98.96275989167457),
    @(20.263462471397375, -98.96263651005681),
    @(20.2634071148333, -98.96285108678335),
    @(20.263356790667, -98.96310857885523),
    @(20.263346725831784, -98.96314612978236),
    @(20.26323098017988, -98.96362892741712),
    @(20.263095104739214, -98.96395079250694),
    @(20.262550689769178, -98.9651588614352),
    @(20.262460659566592, -98.96523083832463),
    @(20.262336867952776, -98.96562671121656),
    @(20.261976746332984, -98.96655041463102),
    @(20.26177417755466, -98.96712622974651),
    @(20.261369039204858, -98.96827785997753),
    @(20.26118897737662, -98.96881768664832),
    @(20.26076132968128, -98.9697893745364),
    @(20.260570013232776, -98.97019724357655),
    @(20.260412458333413, -98.97055712802374),
    @(20.26036744261852, -98.97080904713678),
    @(20.260209887513543, -98.97116893158397),
    @(20.259658443386733, -98.97262046552098),
    @(20.25961342743203, -98.97280040764485),
    @(20.2594221095687, -98.9734242073533),
    @(20.25941085556938, -98.97343620350156),
    @(20.25929831553148, -98.97382008024522),
    @(20.259152013360218, -98.97397603017235),
    @(20.258836900523008, -98.97474378365969),
    @(20.258769376260386, -98.97497171047624),
    @(20.258611819533375, -98.97522362958927),
    @(20.25845426264646, -98.9756554909259),
    @(20.25828545151873, -98.97608735226254),
    @(20.25815040245206, -98.97615932905994),
    @(20.258037861500355, -98.97665117113776),
    @(20.25794782868025, -98.97665117113776),
    @(20.257846541695223, -98.97717900166032),
    @(20.257711492279046, -98.9772029939568),
    @(20.257745254644103, -98.97741892462511),
    @(20.257610205139812, -98.97770683218286),
    @(20.25726132670997, -98.97834262803957),
    @(20.256979972566423, -98.9791703622681),
    @(20.256619838518652, -98.97995011190368),
    @(20.256406008532526, -98.98053792316743),
    @(20.256158415549073, -98.98110174213471),
    @(20.25603461890928, -98.98123369976533),
    @(20.255933330626966, -98.98156959174189),
    @(20.2558095338077, -98.98186949544785),
    @(20.255505668469187, -98.98261325663873),
    @(20.255078005133416, -98.98336901397785),
    @(20.25481915570002, -98.98396882138981),
    @(20.254830410032188, -98.98406479057574),
    @(20.254650340619673, -98.9843526981335),
    @(20.254267692424694, -98.98530039384443),
    @(20.254346473012507, -98.98588820510818),
    @(20.254335218645277, -98.98652400096488),
    @(20.254346473012507, -98.9869198738568),
    @(20.254301455538656, -98.98748369282406),
    @(20.254290201168153, -98.9877116196406),
    @(20.254245183677977, -98.98802351949485),
    @(20.254301455537178, -98.98769962341656),
    @(20.254245183676503, -98.98892323053701),
    @(20.25427894679535, -98.98933109957716),
    @(20.25431270990687, -98.9901588338057),
    @(20.25432396427574, -98.99084261425536),
    @(20.2543352186438, -98.99096257573775),
    @(20.254346473011044, -98.99055470669762),
    @(20.25429020116668, -98.99090259499656),
    @(20.254335218644552, -98.99079462950803),
    @(20.254245183677252, -98.99173032907072),
    @(20.254245183677252, -98.99198224818375),
    @(20.254256438051012, -98.99267802478165),
    @(20.25430145553793, -98.99316986685949),
    @(20.254278946796113, -98.99318186300772),
    @(20.254346473011797, -98.99343378212077),
    @(20.254391490472596, -98.99412955871867),
    @(20.25442525355964, -98.99442946242466),
    @(20.254459016639338, -98.9949572929472),
    @(20.254413999198103, -98.99535316583912),
    @(20.254413999198103, -98.99594097710286),
    @(20.25432396427649, -98.99621688851236),
    @(20.254459016639338, -98.99657677295957),
    @(20.254402744835758, -98.99706861503738),
    @(20.25438023610862, -98.99728454570572),
    @(20.254413999198103, -98.99756045711523),
    @(20.254402744835758, -98.99784836467298),
    @(20.254335218644552, -98.99849615667793),
    @(20.254481525349465, -98.99753646465777),
    @(20.254436507914768, -98.99763243384368),
    @(20.254436507914768, -98.9976924145849),
    @(20.254368981738246, -98.9982682297004),
    @(20.254380236103035, -98.99860412185112),
    @(20.254290201161844, -98.9989640062983),
    @(20.254200166168438, -98.9997797443786),
    @(20.254076367967272, -99.00003166349164),
    @(20.254110131122825, -99.0003555594941),
    @(20.254053859192823, -99.00027158645642),
    @(20.25391880647757, -99.00106333224025),
    @(20.253851280075903, -99.00172312039342),
    @(20.253569919719308, -99.00233492382438),
    @(20.253389848844996, -99.00303070042229),
    @(20.2533223222133, -99.00359451938955),
    @(20.25323228665868, -99.00405037302266),
    @(20.253063469853075, -99.00490209954768),
    @(20.252680817747528, -99.00604173363045),
    @(20.252725835691237, -99.0066295448942),
    @(20.252568272817307, -99.00695344081613),
    @(20.25243321880999, -99.00758923667283),
    @(20.252298164685204, -99.00820104023306),
    @(20.25198303792859, -99.00937666272216),
    @(20.2517917106625, -99.00994048168944),
    @(20.250080724447038, -99.00551153114846),
    @(20.248910222583717, -99.00496570120438),
    @(20.24708129576269, -99.00215857577776),
    @(20.24708129576269, -98.9997413288826),
    @(20.24495971367173, -98.99927347464485),
    @(20.243423377518138, -98.9999752560015),
    @(20.242545464323438, -99.0014567944211),
    @(20.241301745472608, -99.00215857577776),
    @(20.240131177460075, -99.00270440572183),
    @(20.238887439284742, -99.00418594414143),
    @(20.238009500461807, -99.00761687521842),
    @(20.23691206995853, -99.0095662678758),
    @(20.23515616503493, -99.01362100460314),
    @(20.234717185704497, -99.01479064019757),
    @(20.23435136864876, -99.01650610573607),
    @(20.23369289577886, -99.01783169274307),
    @(20.233327076050827, -99.0179876440038),
    @(20.232229612486435, -99.01806561971009),
    @(20.231936954227404, -99.0179876440038),
    @(20.230327323954718, -99.01868942536045),
    @(20.229229839213886, -99.01923525530452),
    @(20.228425012147042, -99.02001501236747),
    @(20.227986013809232, -99.02032691519264),
    @(20.22659584422947, -99.02024893948635),
    @(20.226303175365874, -99.02063881801783),
    @(20.224473982489148, -99.02048286660525),
    @(20.22388863622459, -99.02165250219966),
    @(20.222791106040667, -99.02196440502485),
    @(20.221693568111952, -99.02141857508077),
    @(20.222059414948703, -99.02048286660525),
    @(20.22066919239127, -99.01892335247933),
    @(20.218620420712238, -99.01931323101081),
    @(20.218327736841154, -99.01837752253526),
    @(20.217961881227986, -99.01658408129047),
    @(20.217376510457356, -99.01440076151421),
    @(20.21671796570776, -99.01042400049316),
    @(20.21554721260375, -99.006681166591),
    @(20.215108177918598, -99.00395201687066),
    @(20.21635210628638, -99.0095662681057),
    @(20.215839901682937, -99.0081627053924),
    @(20.214961832725564, -99.00465379860913),
    @(20.21481548741758, -99.00278238165804),
    @(20.214522796388714, -99.00114489182583),
    @(20.214156931828413, -99.00020918335031),
    @(20.215693557200822, -98.9999752562314),
    @(20.21679113746155, -99.00005323193771),
    @(20.218254565764656, -99.0002871590566),
    @(20.221327720391994, -99.00005323193771),
    @(20.223303287734282, -99.0002871590566),
    @(20.226669011336615, -98.9999752562314),
    @(20.22901034131338, -99.00020918335031),
    @(20.23149796578313, -99.0002871590566),
    @(20.23288809153212, -99.00005323193771),
    @(20.23361973167008, -98.99935145058103),
    @(20.23435136836438, -98.99825979069291),
    @(20.23493667559461, -98.9981818151132),
    @(20.23815582401332, -98.9981818151132),
    @(20.240058016736423, -98.99857169364468),
    @(20.241960186174293, -98.99849371793839),
    @(20.24364285511163, -98.99888359646985),
    @(20.245764455187086, -98.99935145070762),
    @(20.2473007681882, -98.99942942641391),
    @(20.24788602628704, -99.00340618743498),
    @(20.24978809987816, -99.00535558009234),
    @(20.251543839440572, -99.00558950721124),
    @(20.252933785849905, -99.00535558009234),
    @(20.25344586823298, -99.0029383331972),
    @(20.253957948927276, -99.00169072189648),
    @(20.254689489846733, -98.99732408234395),
    @(20.254396873892553, -98.99412707838586),
    @(20.254470027932793, -98.99272351567255),
    @(20.254470027932793, -98.99093007442775),
    @(20.254250565708645, -98.98835687612002),
    @(20.254470027932793, -98.98593962922487),
    @(20.254908951450496, -98.9836783337423),
    @(20.256079408098184, -98.98110513543456),
    @(20.255421027484697, -98.98289857733003),
    @(20.25622571472386, -98.98118311179152),
    @(20.25754246666434, -98.97837598636491),
    @(20.25849344723121, -98.97603671517605),
    @(20.259883331426412, -98.97237185698019),
    @(20.26061484442528, -98.9705784157354),
    @(20.26112690147325, -98.9690189016095),
    @(20.26127320317669, -98.96831712025283),
    @(20.261638956831938, -98.9673814117773),
    @(20.262370461556735, -98.96621177618286),
    @(20.263248262675503, -98.96379452928771),
    @(20.262224161089602, -98.96589987375705),
    @(20.26361401187837, -98.96192311273597),
    @(20.264345507294138, -98.95966181725342),
    @(20.265076999261918, -98.95825825454013),
    @(20.265076999261918, -98.95818027883381),
    @(20.26580848778161, -98.95630886188273),
    @(20.26558904158775, -98.95716659465198),
    @(20.266393676114678, -98.95545112911348),
    @(20.266759417702154, -98.95451542063795),
    @(20.2674271454476326, -98.95318983363093),
    @(20.268807554660444, -98.95092853814836),
    @(20.269319584675568, -98.94968092684766),
    @(20.268840727248296, -98.9492536523099),
    @(20.267955050551016, -98.9488244988568),
    @(20.267471952039756, -98.94860992213025),
    @(20.2663359811695, -98.94796000682675),
    @(20.26594920596717, -98.94779508718803),
    @(20.266284411198228, -98.94790503361382),
    @(20.266181271204257, -98.94743776130413),
    @(20.266232841209817, -98.94710792202669),
    @(20.266258626206152, -98.94672310953636)

)


# Índice inicial
$index = 0

# URL del servidor Flask
$flaskUrl = "http://127.0.0.1:443/local"  # Cambia esto a la URL de tu servidor Flask

$fingerprint = "huella_digital_encriptada"

$i = 0

$id = "190"

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

