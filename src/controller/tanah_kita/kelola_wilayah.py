from datetime import datetime
import json
import time
from loguru import logger
import requests
from bs4 import BeautifulSoup
from src.lib.storage_manager import StorageManager
import greenstalk

beanstalk = greenstalk.Client(('192.168.99.69', 11300), watch='sc-tanah-kita-baselink')

class KelolaWilayah:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cookie': 'PHPSESSID=lmicch7idg78skrfp64lpagqq0; lf_ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%222c9209e717edb84ba9d344af63b563c9%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22103.121.213.205%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A101%3A%22Mozilla%2F5.0+%28X11%3B+Linux+x86_64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F128.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1728541108%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D20a457cb79c8a60bef58fa70e9f6c482',
            'priority': 'u=0, i',
            'referer': 'https://tanahkita.id/data/wilayah_kelola/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }

        self.cookies = {
            'PHPSESSID': 'lmicch7idg78skrfp64lpagqq0',
            'lf_ci_session': 'a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%222c9209e717edb84ba9d344af63b563c9%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22103.121.213.205%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A101%3A%22Mozilla%2F5.0+%28X11%3B+Linux+x86_64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F128.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1728541108%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D20a457cb79c8a60bef58fa70e9f6c482',
        }

    def getDetailOne(self, url, tahun, jenis_wikera, kode_prov):
        url = url.replace('index/data/wilayah_kelola/', '')
        
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Mencari container utama
        container = soup.find(class_='content')

        if container:
            self.title = container.find('strong').text if container.find('strong') else 'Unknown'
            
            daatas = {
                "link": url,
                "tags": ["tanahkita"],
                "source": "tanahkita.id",
                'title': "Data Wilayah Kelola",
                'longitude': container.find(id='x').get('value') if container.find(id='x') else None,
                'latitude': container.find(id='y').get('value') if container.find(id='y') else None,
                "sub_title": None,
                "range_data": tahun,
                "create_date": None,
                "update_date": None,
                "desc": None,
                "category": None,
                "sub_category": None,
                "crawling_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "crawling_time_epoch": int(time.time()),
                "table_name": None,
                "country_name": "Indonesia",
                "level": "Nasional",
                "stage": "Crawling data",
            }

            # Menambahkan data dari tabel
            table = container.find('table', class_='table-condensed')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        key = cols[0].text.strip().lower().replace(' ', '_')
                        value = cols[2].text.strip().replace('\xa0', '')
                        daatas[key] = value

            # Memeriksa sumber data
            sumber_data_th = container.find('th', text="Sumber Data")
            if sumber_data_th:
                sumber_data = sumber_data_th.find_next('td').text.strip()
                daatas['sumber_data'] = sumber_data
            else:
                daatas['sumber_data'] = None

            return daatas
        else:
            logger.error(f"Container tidak ditemukan pada URL: {url}")
            return None

    def process(self):
        while True:
            job = beanstalk.reserve()
            success = json.loads(job.body)

            if success:
                url = success['url']
                tahun = success['tahun']
                jenis_wikera = success['jenis_wikera']
                kode_prov = success['kd_prop']

                data = self.getDetailOne(url, tahun, jenis_wikera, kode_prov)

                file_name = f'{data["provinsi"]}_{data["kabupaten"]}_{data["kecamatan"]}_{data["desa"]}_{data["jenis_wilayah_kelola"]}_{data["tahapan"]}_{tahun}'
                path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/tanahkita/wilayah_kelola/{data["tahapan"]}/json/{file_name.replace(" ", "_").replace("/", "_")}.json'
                StorageManager().save_json(path_file, data)
                if data:
                    beanstalk.delete(job)
                    logger.success(f"Success: {file_name}")
                    logger.info(data)
                else:
                    beanstalk.bury(job)
                    logger.error(f"Failed: {url}")
                    break
            else:
                logger.error("Job failed or malformed")
                beanstalk.bury(job)
                break
