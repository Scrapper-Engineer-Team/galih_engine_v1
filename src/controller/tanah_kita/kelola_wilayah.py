from datetime import datetime
import json
import re
import time
from loguru import logger
import requests
from bs4 import BeautifulSoup
from src.lib.storage_manager import StorageManager
import greenstalk

class KelolaWilayah:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.session = requests.Session()

    def clean_text(self, text):
        if isinstance(text, str):
            # Menghapus karakter whitespace ekstra dan menghilangkan karakter non-printable
            text = re.sub(r'\s+', ' ', text)  # Mengganti beberapa spasi dengan satu spasi
            text = text.strip()  # Menghapus spasi di awal dan akhir
            text = re.sub(r'[^\x20-\x7E]', '', text)  # Menghapus karakter non-printable
        return text

    def getDetailOne(self, url, tahun, jenis_wikera, kode_prov, profile):
        url = url.replace('index/data/wilayah_kelola/', '')
        response = self.session.get(url, headers=self.headers, timeout=30)
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Mencari container utama
        container = soup.find(class_='content')

        longitude = container.find(id='x').get('value')
        latitude = container.find(id='y').get('value')
        
        keys = container.select('table.table-condensed tr td.table_title')
        keys2 = container.select('table tr th')

        values = container.select('table.table-condensed tr td:nth-child(3)')
        values2 = container.select('div.col-md-12 table tr td')

        key_list = []
        value_list = []
        for key, key2, value, value2 in zip(keys, keys2, values, values2):
            key_list.append(key.text)
            key_list.append(key2.text)

            value_list.append(value.text)
            value_list.append(value2.text)

        datas = {}
        for key, value in zip(key_list, value_list):
            datas[self.clean_text(key.lower().replace(' ', '_'))] = value
        
        # Membersihkan data
        cleaned_data = {key: self.clean_text(value) for key, value in datas.items()}
        cleaned_data['url'] = url
        cleaned_data['tahun'] = tahun
        cleaned_data['jenis_wikera'] = jenis_wikera
        cleaned_data['kd_prop'] = kode_prov
        cleaned_data['latitude'] = latitude
        cleaned_data['longitude'] = longitude
        cleaned_data['profile'] = profile

        file_name = f"{cleaned_data.get('provinsi', None)}_{cleaned_data.get('kabupaten', None)}_{cleaned_data.get('kecamatan', None)}_{cleaned_data.get('desa', None)}_{cleaned_data.get('jenis_wilayah_kelola', None)}_{cleaned_data.get('tahapan', None)}_{tahun}"
        path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/tanahkita/wilayah_kelola/{cleaned_data["tahapan"].replace(" ", "_").lower()}/json/{file_name.replace(" ", "_").replace("/", "_").lower()}.json'
        metadata = {
            "link": url,
            "tags": [
                "tanah_kita",
                "wilayah_kelola",
                f'{cleaned_data["tahapan"].replace(" ", "_").lower()}'
            ],
            "source": "tanahkita.id",
            "title": "Data Wilayah Kelola",
            "sub_title": None,
            "range_data": tahun,
            "create_date": None,
            "update_date": None,
            "desc": None,
            "category": "Wilayah Kelola",
            "sub_category": None,
            "data": cleaned_data,
            "path_data_raw": [
                path_file
            ],
            "crawling_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "crawling_time_epoch": int(time.time()),
            "table_name": None,
            "country_name": "Indonesia",
            "level": "Nasional",
            "stage": "Crawling data",
            "update_schedule": "yearly"
        }

        StorageManager().save_json(path_file, metadata)
        print(metadata)
        return True

    def process(self):
        beanstalk = greenstalk.Client(('192.168.99.69', 11300), watch='sc-tanah-kita-baselink')
        
        while True:
            job = beanstalk.reserve()
            success = json.loads(job.body)

            if success:
                url = success['url']
                tahun = success['tahun']
                jenis_wikera = success['jenis_wikera']
                kode_prov = success['kd_prop']
                profile = success['profile']

                data = self.getDetailOne(url, tahun, jenis_wikera, kode_prov, profile)

                if data:
                    beanstalk.delete(job)
                    logger.success(f"Success save json!")
                    logger.info(data)
                else:
                    beanstalk.bury(job)
                    logger.error(f"Failed: {url}")
            else:
                logger.error("Job failed or malformed")
                beanstalk.bury(job)