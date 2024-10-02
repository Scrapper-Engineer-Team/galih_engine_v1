from datetime import datetime
import time

from loguru import logger
import requests
from src.lib.beautifulsoup_engine import Soup
from src.lib.storage_manager import StorageManager

class YearBook:
    def __init__(self, url):
        self.soup = Soup(url)
        
    def get_title(self):
        titles = self.soup.select('h5.title')
        for title in titles:
            yield title.text

    def get_link(self):
        links = self.soup.select('li div a')
        for link in links:
            if 'href' in link.attrs:
                yield link['href']

    def download(self):
        for link, title in zip(self.get_link(), self.get_title()):
            filename = title.lower().replace(" ", "_").replace("/", "_")
            path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/komisi_yudisial/year_book/pdf/{filename}.pdf'
            path_json = f's3://ai-pipeline-raw-data/data/data_descriptive/komisi_yudisial/year_book/json/{filename}.json'

            response = requests.get(f"https://komisiyudisial.go.id{link}")
            StorageManager().save(path_file, response)
            logger.success(f"File saved: {path_file}")

            metadata = {
                "link": link,
                "tags": [
                    "komisi_yudisial",
                    "year_book"
                ],
                "source": "komisiyudisial.go.id",
                "title": title,
                "sub_title": None,
                "range_data": None,
                "create_date": None,
                "update_date": None,
                "desc": None,
                "category": "Year Book",
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

            logger.success(f"Metadata saved: {path_json}")