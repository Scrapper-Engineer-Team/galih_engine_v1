from datetime import datetime
import json
import time
from loguru import logger
import requests
from src.lib.beautifulsoup_engine import Soup
from src.lib.storage_manager import StorageManager

class InfografisKy:

    def __init__(self, url):
        self.soup = Soup(url)

    def get_title(self):
        titles = self.soup.select('p.description strong')
        for title in titles:
            yield title.text

    def get_images(self):
        images = self.soup.select('img.tai')
        for image in images:
            yield image['src']

    def download(self):
        for title, image in zip(self.get_title(), self.get_images()):
            data={
                'title': title,
                'image': f"https://komisiyudisial.go.id{image}"
            }
            print(data)

            file_name = title.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
            path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/komisi_yudisial/infografis/image/{file_name}.png'
            path_json = f's3://ai-pipeline-raw-data/data/data_descriptive/komisi_yudisial/infografis/json/{file_name}.json'

            response = requests.get(data['image'])
            StorageManager().save(path_file, response)
            logger.success(f"File saved: {path_file}")

            metadata = {
                "link": data['image'],
                "tags": [
                    "komisi_yudisial",
                    "infografis"
                ],
                "source": "komisiyudisial.go.id",
                "title": data['title'],
                "sub_title": None,
                "range_data": None,
                "create_date": None,
                "update_date": None,
                "desc": None,
                "category": "Infografis",
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

            StorageManager().save_json(path_json, json.dumps(metadata))
            logger.success(json.dumps(metadata))