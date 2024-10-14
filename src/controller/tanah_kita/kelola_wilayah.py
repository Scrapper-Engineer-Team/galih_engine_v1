from datetime import datetime
import json
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

    def getDetailOne(self, url, tahun, jenis_wikera, kode_prov):
        url = url.replace('index/data/wilayah_kelola/', '')
        response = self.session.get(url, headers=self.headers, timeout=30)
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Mencari container utama
        container = soup.find(class_='content')

        longitude = container.find(id='x').get('value')
        latitude = container.find(id='y').get('value')
        
        keys = container.select('table.table-condensed tr td.table_title')
        keys2 = container.select('table tr td')

        for key in zip(keys, keys2):
            print(key.text)

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

                data = self.getDetailOne(url, tahun, jenis_wikera, kode_prov)

                if data:
                    file_name = f"{data.get('provinsi', 'Unknown')}_{data.get('kabupaten', 'Unknown')}_{data.get('kecamatan', 'Unknown')}_{data.get('desa', 'Unknown')}_{data.get('jenis_wilayah_kelola', 'Unknown')}_{data.get('tahapan', 'Unknown')}_{tahun}"
                    path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/tanahkita/wilayah_kelola/{data["tahapan"]}/json/{file_name.replace(" ", "_").replace("/", "_")}.json'
                    StorageManager().save_json(path_file, data)
                    beanstalk.bury(job)
                    logger.success(f"Success: {file_name}")
                    logger.info(data)
                else:
                    beanstalk.bury(job)
                    logger.error(f"Failed: {url}")
            else:
                logger.error("Job failed or malformed")
                beanstalk.bury(job)