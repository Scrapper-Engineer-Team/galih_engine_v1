from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
from src.lib.storage_manager import StorageManager

class Indicator:
    def __init__(self):
        self.cookies = {
            '_ga': 'GA1.1.501987845.1726637118',
            '_ga_LR61RNZPPN': 'GS1.1.1726637118.1.0.1726637118.60.0.0',
            'cookie_BIWEB': '!qhGvOXHoLi+LTy7t0q10PaN+sDuIGEWziEHZ+D96uQPPrLwNZved6pkgDLJqppn9REfPY55kddmIaw==',
            'WSS_FullScreenMode': 'false',
            'TS014171ca': '0199782b6f728a0341d1c46f49ba2cd76b0a5e668e8a7f6eb096a82bdd60c3fbf8def5408ebb9acd26e9ee752fb06bf38fbbf84f88',
            'TS0dddebd2027': '08f7caa0deab2000e67f95fe2271d3c3358472411b3444dc986a1d463fedf71a9640b631dcb34d9908ccec4db31130009e6f6fa739298cec618db19b219ef72036cf0543576658f23cd2667408a10cf27d2efb65b94fd928b884f8f08c4abbdc',
        }

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': '_ga=GA1.1.501987845.1726637118; _ga_LR61RNZPPN=GS1.1.1726637118.1.0.1726637118.60.0.0; cookie_BIWEB=!qhGvOXHoLi+LTy7t0q10PaN+sDuIGEWziEHZ+D96uQPPrLwNZved6pkgDLJqppn9REfPY55kddmIaw==; WSS_FullScreenMode=false; TS014171ca=0199782b6f728a0341d1c46f49ba2cd76b0a5e668e8a7f6eb096a82bdd60c3fbf8def5408ebb9acd26e9ee752fb06bf38fbbf84f88; TS0dddebd2027=08f7caa0deab2000e67f95fe2271d3c3358472411b3444dc986a1d463fedf71a9640b631dcb34d9908ccec4db31130009e6f6fa739298cec618db19b219ef72036cf0543576658f23cd2667408a10cf27d2efb65b94fd928b884f8f08c4abbdc',
            'If-Modified-Since': 'Mon, 14 Oct 2024 04:13:28 GMT',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }
    
    def get_html(self):
        response = requests.get('https://www.bi.go.id/id/statistik/indikator/Default.aspx', cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return soup

    def get_title(self):
        title = self.get_html().select_one('div.ms-rtestate-field h2')

        title_text = title.text
        title_text = title_text.replace('\u200b', '').replace('\n', '')

        return title_text
    
    def get_description(self):
        description = self.get_html().select_one('div.ms-rtestate-field div')
        description_text = description.text
        description_text = description_text.replace('\u200b', '').replace('\n', '')
        
        return description_text
    
    def get_data(self):
        # Find all the boxes
        boxes = self.get_html().find_all('div', class_='box-list')
        urls = self.get_html().find_all('a', class_='box-list__hyperlink')

        for box, url in zip(boxes, urls):
            # Safeguard to check if 'p' and 'h2' exist
            title_tag = box.find('p')
            value_tag = box.find('h2')
            date_tag = box.find_all('p')

            title = title_tag.get_text(strip=True) if title_tag else 'N/A'
            value = value_tag.get_text(strip=True) if value_tag else 'N/A'
            date = date_tag[1].get_text(strip=True) if len(date_tag) > 1 else 'N/A'
            

            # Filter out entries where value is 'N/A'
            if value != 'N/A':
                data_list ={
                    'title': title,
                    'value': value,
                    'date': date,
                    'url': f"https://www.bi.go.id/{url.get('href')}"
                }
                yield data_list

    
    def process(self):
        for data in self.get_data():
            print(data)
            yield data