from datetime import datetime
import json
import time

from loguru import logger
import requests
from src.lib.beautifulsoup_engine import Soup
from src.lib.storage_manager import StorageManager

class JurnalIlmiahGeomatika:
    def __init__(self, url):
        self.url = url
        self.soup = Soup(url)
        
    def get_links(self):
        links = self.soup.select('td a')
        link_list = []
        for link in links:
            if 'pdf' in link['href']:
                link_text = f"https://big.go.id{link['href']}"
                link_list.append(link_text)
        return link_list
    
    def get_titles(self):
        titles = self.soup.select('td strong')
        title_list = []
        for t in titles:
            if 'Table of Contents' not in t.text:
                title_list.append(t.text)
        return title_list
    
    def download(self):
        for link, title in zip(self.get_links(), self.get_titles()):
            file_name = title.lower().replace('\r', '').replace('\n', '').replace('\t', '')
            path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/big/jurnal_ilmiah_geomatika/pdf/{file_name}.pdf'
            json_file = f's3://ai-pipeline-raw-data/data/data_descriptive/big/jurnal_ilmiah_geomatika/json/{file_name}.json'
            
            response = requests.get(link)
            # Menggunakan StorageManager untuk mengunduh file
            StorageManager().save(path_file, response)
            logger.success(f'Downloaded to local : {path_file}')

            metadata = {
                "link": link,
                "tags": [
                    "badan_informasi_geopasial",
                    "jurnal_ilmiah_geomatika"
                ],
                "source": "big.go.id",
                "title": title,
                "sub_title": None,
                "range_data": None,
                "create_date": None,
                "update_date": None,
                "desc": None,
                "category": "Jurnal Ilmiah Geomatika",
                "sub_category": None,
                "path_data_raw": [
                    path_file,
                    json_file
                ],
                "crawling_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "crawling_time_epoch": int(time.time()),
                "table_name": "judul_tabel",
                "country_name": "Indonesia",
                "level": "Nasional",
                "stage": "Crawling data",
                "update_schedule": "daily"
            }

            StorageManager().save_json(json_file, metadata)
            logger.success(json.dumps(metadata))


    def process(self):
        self.download()