from datetime import datetime
import json
import time
from bs4 import BeautifulSoup
from loguru import logger
import requests
from src.lib.storage_manager import StorageManager

class LaporanKeuanganKpu:
    def __init__(self) -> None:
        self.cookies = {
            'cookiesession1': '678B2874D9EA9C75AD185714AE196B3E',
            'XSRF-TOKEN': 'eyJpdiI6IlNnRWtTc1ZxMW9yQXp0b2N5cXlTUFE9PSIsInZhbHVlIjoiY2ZsMGw3NXhKTW91XC9TK0VrdGVGc0t2bVV5dW1tXC9BVnh3ZUNmZitNOEJxNndUSGJsS2ZHYjFtNHFFd1ZpMXFqIiwibWFjIjoiNmM0NzU1NjMxZDg3N2QyMDRjYTUxMmIzN2FmNWFjOTJiNzNiN2U1NmMyYjE4YjAzMGEwMTQwYmZiZWIzNWI1MSJ9',
            'laravel_session': 'eyJpdiI6IkJNeVd1M05LT0ZCck8zQWJ5TG95QVE9PSIsInZhbHVlIjoiZXM5S0FqZVZUMWU1a2FvSVdieWhOczJiaFN4Mk9DMStMM1N0OFJ2Tml3bHJCZTZwTWFNaXNHMWt6bndCamVOMSIsIm1hYyI6IjQxYWQ0YmM5N2Y5ZWViODhiNDMxZjU0MjRiOGM1ODlmMGZlNTAzOGRiZjRkNTIwYzI3MWI0MmQwNTk2NDEwMDMifQ%3D%3D',
        }

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': 'cookiesession1=678B2874D9EA9C75AD185714AE196B3E; XSRF-TOKEN=eyJpdiI6IlNnRWtTc1ZxMW9yQXp0b2N5cXlTUFE9PSIsInZhbHVlIjoiY2ZsMGw3NXhKTW91XC9TK0VrdGVGc0t2bVV5dW1tXC9BVnh3ZUNmZitNOEJxNndUSGJsS2ZHYjFtNHFFd1ZpMXFqIiwibWFjIjoiNmM0NzU1NjMxZDg3N2QyMDRjYTUxMmIzN2FmNWFjOTJiNzNiN2U1NmMyYjE4YjAzMGEwMTQwYmZiZWIzNWI1MSJ9; laravel_session=eyJpdiI6IkJNeVd1M05LT0ZCck8zQWJ5TG95QVE9PSIsInZhbHVlIjoiZXM5S0FqZVZUMWU1a2FvSVdieWhOczJiaFN4Mk9DMStMM1N0OFJ2Tml3bHJCZTZwTWFNaXNHMWt6bndCamVOMSIsIm1hYyI6IjQxYWQ0YmM5N2Y5ZWViODhiNDMxZjU0MjRiOGM1ODlmMGZlNTAzOGRiZjRkNTIwYzI3MWI0MmQwNTk2NDEwMDMifQ%3D%3D',
            'Referer': 'https://www.kpu.go.id/page/read/383/laporan-realisasi-anggaran-kpu',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'X-XSRF-TOKEN': 'eyJpdiI6IlNnRWtTc1ZxMW9yQXp0b2N5cXlTUFE9PSIsInZhbHVlIjoiY2ZsMGw3NXhKTW91XC9TK0VrdGVGc0t2bVV5dW1tXC9BVnh3ZUNmZitNOEJxNndUSGJsS2ZHYjFtNHFFd1ZpMXFqIiwibWFjIjoiNmM0NzU1NjMxZDg3N2QyMDRjYTUxMmIzN2FmNWFjOTJiNzNiN2U1NmMyYjE4YjAzMGEwMTQwYmZiZWIzNWI1MSJ9',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }


    def get_data(self):
        response = requests.get('https://www.kpu.go.id/api/page/383/read', cookies=self.cookies, headers=self.headers)
        data = response.json()

        return data
    
    def get_titles_and_links(self):
        data = self.get_data()
        if data is None:
            return  # Jika tidak ada data, keluar dari fungsi

        pages_desc = data['data']['pages_desc']
        
        # Menggunakan BeautifulSoup untuk mem-parsing HTML
        soup = BeautifulSoup(pages_desc, 'html.parser')
        
        for item in soup.find_all('p',):  # Ganti 'item-class' dengan class yang sesuai untuk setiap item
            title_span = item.find('span')  # Mengambil title dari elemen <span>
            link_a = item.find('a')  # Mengambil link dari elemen <a>

            title = title_span.text.strip() if title_span else None
            url = link_a['href'] if link_a and 'href' in link_a.attrs else None
            
            if title and url:  # Pastikan title dan url tidak kosong
                yield {
                    'title': title,
                    'url': url
                }
    
    def download(self):
        for title in self.get_titles_and_links():
            file_name = f'{title["title"].lower().strip().replace(" ", "_").replace("/", "_").replace("_klik_di_sini", "_")}'
            path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/kpu/laporan_keuangan/pdf/{file_name}.pdf'
            path_json = f's3://ai-pipeline-raw-data/data/data_descriptive/kpu/laporan_keuangan/json/{file_name}.json'
            if title['url'].endswith('.pdf'):
                response = requests.get(title['url'])
                StorageManager().save(path_file, response)
                logger.success(f'Downloaded to local : {path_file}')

                metadata = {
                    "link": title['url'],
                    "tags": [
                        "kpu",
                        "laporan_keuangan"
                    ],
                    "source": "kpu.go.id",
                    "title": title["title"].replace("KLIK DI SINI", ""),
                    "sub_title": None,
                    "range_data": None,
                    "create_date": None,
                    "update_date": None,
                    "desc": None,
                    "category": "Laporan Keuangan",
                    "sub_category": None,
                    "path_data_raw": [
                        path_file,
                        path_json
                    ],
                    "crawling_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "crawling_time_epoch": int(time.time()),
                    "table_name": "judul_tabel",
                    "country_name": "Indonesia",
                    "level": "Nasional",
                    "stage": "Crawling data",
                    "update_schedule": "daily"
                }

                StorageManager().save_json(path_json, metadata)
                logger.success(f'Downloaded to local : {path_json}')