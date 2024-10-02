import json
import requests

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

data = {
    'x': '113.57648849487305',
    'y': '-1.3692124638621377',
    # 'z': '0.18453598022460938',
    # 'w': '1075',
    'mz': '18',
    'idL': '||||||1|||||||',
    'idP': 'i_jalan|i_prm|i_sp|i_wst|i_bum|i_pru|i_rtsp|i_rskp|info4|info2|info8|infokp|info',
    'idR': '10-21|10-21|10-18|4-21|4-21|4-21|10-18|10-18|4-17|4-18|6-21|6-21|6-21',
}

response = requests.post('https://sipukat.kemendesa.go.id/i.php', headers=headers, data=data)
data = json.loads(response.text)

print(data)