import json
import requests

class Rtsp:
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Content-Length': '0',
            'Origin': 'https://sipukat.kemendesa.go.id',
            'Referer': 'https://sipukat.kemendesa.go.id/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }
    
    def get_response(self):
        response = requests.post('https://inarisk.bnpb.go.id:444/dashboardkegiatan/data/lapor_kejadian_get_json.php', headers=self.headers, verify=False)
        datas = json.loads(response.text)
        print(json.dumps(datas))
    
    def process(self):
        self.get_response()