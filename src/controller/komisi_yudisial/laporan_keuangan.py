from datetime import datetime
import json
import time

from loguru import logger
import requests
from src.lib.beautifulsoup_engine import Soup
from src.lib.storage_manager import StorageManager

class LaporanKeuanganKy:
    def __init__(self, url):
        self.soup = Soup(url)

    def get_data(self):
        datas = self.soup.select('article.post div a')
        for data in datas:
            data = {
                'title': data.text.strip(),
                'url': f"https://komisiyudisial.go.id/{data['href'].replace('../../../', '')}"
            }
            yield data

    def process(self):
        for data in self.get_data():
            file_name = data["title"].lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
            path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/komisi_yudisial/laporan_keuangan/pdf/{file_name}.pdf'
            path_json = f's3://ai-pipeline-raw-data/data/data_descriptive/komisi_yudisial/laporan_keuangan/json/{file_name}.json'

            try:
                # Request file with streaming to handle large files
                response = requests.get(data['url'], stream=True)
                response.raise_for_status()  # Raise an error for bad responses

                # Save file using StorageManager
                StorageManager().save(path_file, response)
                print(f"File saved: {path_file}")

                metadata = {
                    "link": data['url'],
                    "tags": [
                        "komisi_yudisial",
                        "laporan_keuangan"
                    ],
                    "source": "komisiyudisial.go.id",
                    "title": data['title'],
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

                StorageManager().save_json(path_json, json.dumps(metadata))
                logger.success(json.dumps(metadata))
                # print(json.dumps(metadata))
            except Exception as e:
                logger.error(e)    