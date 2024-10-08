import ast
import json
from loguru import logger
import requests
import re
from bs4 import BeautifulSoup

lpu = [
    # '1|JANTHO|PADI|95.648974065701|5.2968660250557',
    # '2|PATEK|PADI|95.4780482|4.8697420361446',
    # '3|COT GIREK|KELAPA SAWIT|97.401128123347|4.9376921678535',
    # '4|PINTU RIME GAYO|KOPI|96.739279989393|4.8930953338244',
    # '5|KEDURANG|PADI|103.06321420699|-4.4516323729483',
    # '6|BELANTIKAN RAYA|KARET|111.48250182941|-1.7424877674208',
    # '7|TONGO-SEKONGKANG|JAGUNG|116.89590445278|-9.0389335045807',
    # '8|PETATA|PADI|104.11867|-3.1807962150042',
    # '9|LARANTUKA|HORTIKULTURA (JAMBU METE)|122.83878668271|-8.410552181',
    # '10|JELAI (PULAU NIBUNG)|PADI|110.82867|-2.94293',
    # '11|BAJAWA|KOPI|120.91840027706|-8.6781776530137',
    # '12|MAWASANGKA|HORTIKULTURA (JAMBU METE)|122.37982752753|-5.2859206854419',
    # '13|KUMPEH|KELAPA SAWIT|103.86682764373|-1.4168293989333',
    # '14|SUMALATA|JAGUNG|122.7893|0.89041',
    # '15|PADANG ULAK TANDING|KOPI|102.81402661419|-3.4066017332988',
    # '16|TERENTANG|PADI|109.58752000676|-0.37816896960064',
    # '17|TUMBANG JUTUH - BERENG BELAWAN|KELAPA SAWIT|113.59802209852|-1.3378924285714',
    # '18|LAMBALE|KELAPA|123.08794328205|-4.8217750607287',
    # '19|MENGKENDEK|KOPI|119.91561407164|-3.2107214341058',
    # '20|RANTE KARUA|KOPI|119.77858371083|-2.898156614225',
    # '21|GILIRENG|PADI|120.23025534002|-3.8215160828688',
    # '22|WERIANGGI - WERABUR|HORTIKULTURA (PISANG)|134.23326406164|-2.5566903372781',
    # '23|PAYAHE|KELAPA|127.73425679036|0.24768467773438',
    # '24|KLAMONO-SEGUN|KAKAO|131.4667799565|-1.1841866109728',
    # '25|SEULIMEUM|JAGUNG|95.5898443564|5.4478199507011',
    # '26|KOLONO|KAKAO|122.61547587117|-4.2119694945256',
    # '27|JEBUS|LADA|105.51|-1.7979',
    # '28|MATAN HILIR SELATAN|PADI|110.3020488593|-1.9637272138223',
    # '29|SEBAMBAN|PERIKANAN TANGKAP|115.70888319811|-3.6870253508274',
    # '30|GULA HABANG|KARET|115.47737703168|-2.3636110243902',
    # '31|MUARA KUANG|KARET|104.57873095489|-3.670979887218',
    # '32|PATLEAN|PADI|128.70188545241|1.368276531258',
    # '33|MOMIWAREN|PERIKANAN TANGKAP|134.17095398967|-1.451456681459',
    # '34|SALAKAN|PERIKANAN TANGKAP|123.22499879683|-1.57082333708612',
    # '35|PALOLO|KOPI|120.017|-1.0764431259233',
    # '36|PADAULOYO|KELAPA|121.8646319704|-1.0888630249249',
    # '37|BASIDONDO|CENGKEH|120.68930821411|0.84219432909794',
    # '38|ANAWUA|PADI|121.57311906587|-4.5312829654691',
    # '39|WOYLA|PADI|96.038002784951|4.4596492535271',
    # '40|SAMAR KILANG|KOPI|97.123663747815|4.7182449250152',
    # '41|SUBULUSSALAM|KELAPA SAWIT|97.886194438725|2.6487218327206',
    # '42|MUARA SAHUNG|PADI|103.34120071879|-4.6274974048036',
    # '43|GERAGAI|KELAPA SAWIT|103.7864|-1.191',
    # '44|JAGOI BABANG|PADI|109.8091300043|1.3070694395161',
    # '45|KERANG|KELAPA SAWIT|116.1252689394|-2.1545319780244',
    # '46|KETUNGAU HULU|KELAPA SAWIT|111.18881895873|0.99915082882883',
    # '47|KALUKKU|KAKAO|119.40822054988|-2.5077820081759',
    # '48|SARUDU BARAS|JAGUNG|119.3652354732|-1.5190280260546',
    # '49|ULUIWOI|KELAPA SAWIT|121.543|-3.6905228989187',
    # '50|LASALIMU|KELAPA|123.13155342794|-5.331447579488',
    # '51|ROUTA|KAKAO|121.64442|-3.654',
    # '52|HIALU|CENGKEH|122.16194821095|-3.2976594099417',
    # '53|MARIORIWAWO|KAKAO|119.94344174724|-4.505415762867',
    # '54|MASAMBA|PADI|120.35201676478|-2.502984596401',
    # '55|TANGLAPUI|VANILI|124.63944050031|-8.3655107620795',
    # '56|BENA|PADI|124.39232758358|-10.087317719953',
    # '57|SENGGI|PADI|140.68478461152|-3.4172875174419',
    # '58|BOMBERAY - TOMAGE|PALA|132.90017179922|-2.8333430892565',
    # '59|BUMI ASRI|KELAPA SAWIT|101.44498597382|-1.3812565787538',
    # '60|SEKO|PADI|119.91292965497|-2.2832015672515',
    # '61|LEREH|SAGU|140.06344665084|-3.0103309973862',
    # '62|WERI - SAHAREY|PALA|132.5953575598|-3.135430195342',
    # '63|MENTEBAH|PADI|112.72727418605|0.839116',
    # '64|PITURIASE|PADI|120.02659481206|-3.8023839988627',
    # '65|PULAU RUPAT|KELAPA SAWIT|101.65036006061|1.9865304199134',
    # '66|MUTIARA|KAKAO|122.853291|-4.8267809584578',
    # '67|BATHIN III|JAGUNG|101.89252641218|-1.6818503163673',
    # '68|LATIUNG|KELAPA|96.45109506|2.4096766',
    # '69|HARUS MUDA JAYA|PERIKANAN BUDIDAYA|96.514662724896|5.1431511835774',
    # '70|KETAPANG NUSANTARA|PADI|97.115383944|4.4163367624633',
    # '71|BATHIN IX|PADI|102.92439233|-2.2236372975',
    # '72|SEI MANGGARIS|KELAPA SAWIT|117.3221959091|4.238697158628',
    # '73|LAMUNTI - DADAHUP|PADI|114.64669709172|-2.681985984714',
    # '74|PULAU BACAN|KELAPA|127.39213855522|-0.41527774323578',
    # '75|TOLIWANG|KELAPA|127.97978567586|1.3935316210709',
    # '76|MANGOLI|KELAPA|125.4679|-1.9147',
    # '77|TASIFETO-MANDEU|JAGUNG|125.00362064199|-9.0755926200504',
    # '78|AMFOANG|PETERNAKAN|123.78523652836|-9.6517391578728',
    # '79|KOBALIMA TIMUR|KEMIRI|124.91503|-9.60236',
    # '80|MUTING|PADI|140.63012728535|-7.3968793055556',
    # '81|ULUMANDA|KOPI|118.91194322246|-3.0942881781454',
    # '82|LALUNDU DAN BAMBAKAENU|KOPI|119.70718196464|-1.0671511901141',
    # '83|BUNGKU UTARA|PADI|121.767|-1.744',
    # '84|ULUBONGKA|KELAPA|121.462|-1.0993654967184',
    # '85|TINANGGEA|KAKAO|122.15542964801|-4.3518469295139',
    # '86|SIMPANG RIMAU-MUARA KELINGI|KELAPA SAWIT|103.36984295881|-3.2587574970268',
    # '87|MUARA TAKUNG-KAMANG BARU|KELAPA SAWIT|101.29206751512|-0.75577144936709',
    # '88|WAY KANAN|PADI|104.46957992498|-4.3374581022259',
    # '89|SAGEA WALEH|PALA|128.18117348387|0.50284',
    # '90|KIKIM|KELAPA SAWIT|103.25428078281|-3.704398702403',
    # '91|LABANGKA|JAGUNG|117.80123723861|-8.8196858776816',
    # '92|PONU|PADI|124.58879757196|-9.1707109340045',
    '93|SALIM BATU|PADI|117.45470948271|2.8834779315911',
    # '94|SEKAYAM - ENTIKONG|PADI|110.38422783622|0.89384052451994',
    # '95|LEWA|PADI|119.85066961807|-9.7197930554415',
    # '96|KODI LOURA|HORTIKULTURA (JAMBU METE)|118.99978223179|-9.4994292056146',
    # '97|SABU|PADI|121.87074346471|-10.5417920311',
    # '98|MBAY|KELAPA|121.26900903057|-8.6398795009265',
    # '99|MAUKARO|HORTIKULTURA (JAMBU METE)|121.79146060003|-8.5876742094775',
    # '100|GERBANG MASPERKASA|PADI|109.51546570703|1.684879765223',
    # '101|BATUTUA NUSAMANUK|KACANG TANAH|122.94973160991|-10.923429036638',
    # '102|KARANG AGUNG ILIR|PADI|104.65742702542|-2.2259526186441',
    # '103|TALUDUTI|JAGUNG|121.68008256308|0.54557591583521',
    # '104|PAGUYAMAN PANTAI|JAGUNG|122.53077241364|0.54100053636364',
    # '105|ENGGANO|HORTIKULTURA (PISANG)|102.24875937745|-5.355021812709',
    # '106|LEMBAH SABIL|KAKAO|96.921656834635|3.609667755627',
    # '107|BABAHROT|KAKAO|96.650196297057|3.8378424918823',
    # '108|SELAUT|KELAPA|95.81249657114|2.664403353675',
    # '109|TAMBORA|PADI|118.13048|-8.1510278050363',
    # '110|TUBBI TARAMANU|KAKAO|119.04295428742|-3.2421488858811',
    # '111|KANTISA|JAGUNG|122.48931961416|-4.7596891467577',
    # '112|BANGGAI SELATAN|PERIKANAN TANGKAP|123.11406969435|-1.8420736548152',
    # '113|MAMBI MEHALAAN|KOPI|119.18944286758|-2.952065913',
    # '114|BAHARI TOMINI RAYA|PADI|121.04808705367|0.48541684154672',
    # '115|PULAU MOROTAI|PADI|128.16039848635|2.3427580067114',
    # '116|LUNANG SILAUT|JAGUNG|101.07067743325|-2.3788901545117',
    # '117|MESUJI|KELAPA SAWIT|105.58995911259|-4.0096456196272',
    # '118|LAGITA|KELAPA SAWIT|101.87327881821|-3.3262542784051',
    # '119|TELANG|PADI|104.72247050446|-2.7045111433878',
    # '120|BELITANG|PADI|104.6507169068|-4.0018074745763',
    # '121|PAWONSARI|JAGUNG|122.44216154046|0.7187811628131',
    # '122|PULUBALA|PADI|122.74315446526|0.65357075631579',
    # '123|GERBANG KAYONG|KELAPA SAWIT|109.72998173649|-1.1345717990521',
    # '124|RASAU JAYA|PADI|109.32735570385|-0.23712177721943',
    # '125|CAHAYA BARU|JERUK|114.67262905257|-3.0983445923979',
    # '126|MALOY KALIORANG|KELAPA SAWIT|117.92991860616|0.9166641010263',
    # '127|KOBISONTA|PADI|129.88774397715|-2.9495322769402',
    # '128|LAMBOYA|PADI|119.33853300055|-9.7377717093596',
    # '129|MELOLO|TEBU|120.62537771194|-9.9262964098361',
    # '130|SALOR|PADI|140.19441093232|-8.162168915768',
    # '131|TOBADAK|PADI|119.29910651528|-2.1196436256184',
    # '132|AIR TERANG|JAGUNG|121.37694234909|1.1740864323967',
    # '133|BUNGKU|PADI|121.77512774211|-2.3170293322872',
    # '134|TAMPOLORE|KAKAO|120.32875365557|-1.5267362098408',
    # '135|RAWA PITU|PADI|105.58106332697|-4.2739034179775',
    # '136|MAHALONA|PADI|121.55261402276|-2.5953925259166',
    # '137|BATU BETUMPANG|PADI|106.17412409296|-2.76437460505556',
    # '138|SUBAH|PADI|109.4718885|1.25086875',
    # '139|PARIT RAMBUTAN|KARET|104.65250797552|-3.087602212908',
    # '140|NUSLIKU|KELAPA|127.8691974|-0.069789387643852'
]

latlong = []

for entry in lpu:
    parts = entry.split('|')
    latlong.append({
        "x": float(parts[3]),  # Koordinat X (longitude)
        "y": float(parts[4])   # Koordinat Y (latitude)
    })

headers = {
    'Accept': '*/*',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://sipukat.kemendesa.go.id',
    'Referer': 'https://sipukat.kemendesa.go.id/petaterpadu.php?v=2021',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

for idx,latlong in enumerate(latlong):
    data = {
        'x': f"{latlong['x']}",
        'y': f"{latlong['y']}",
        # 'z': '0.18453598022460938',
        # 'w': '1075',
        'mz': f'15',
        'idL': '||||||1|||||||',
        'idP': 'i_jalan|i_prm|i_sp|i_wst|i_bum|i_pru|i_rtsp|i_rskp|info4|info2|info8|infokp|info',
        'idR': '10-21|10-21|10-18|4-21|4-21|4-21|10-18|10-18|4-17|4-18|6-21|6-21|6-21',
    }

    response = requests.post('https://sipukat.kemendesa.go.id/i.php', headers=headers, data=data)
    datas = response.text
    logger.info(latlong)
    # logger.info(i)
    logger.info(idx)
    if datas:
        data = json.loads(datas)
        soup = BeautifulSoup(data['isi'], 'html.parser')

        titles = soup.select_one('h1')
        key = soup.select('tr td:nth-child(1)')
        value = soup.select('tr td:nth-child(3)')

        isi = {}
        for k, v in zip(key, value):
            data_akhir = {
                'title': titles.text.strip(),
                k.text.strip(): v.text.strip(),
            }
            isi.update(data_akhir)
        data.update({'isi':isi})

        data['pol'] = ast.literal_eval(data['pol'])

        # Membalikkan koordinat di dalam 'pol'
        data['pol'] = [[coord[1], coord[0]] for coord in data['pol']]

        print(data)