import json
import requests
from src.lib.storage_manager import StorageManager
from src.lib.beautifulsoup_engine import Soup
from datetime import datetime
import time

class LaporanKeuangan:
    def __init__(self, url) -> None:
        self.url = url

    def get_data(self):
        soup = Soup(self.url)
        titles = soup.select('td a')
        for title in titles:
            if 'href' in title.attrs:
                data = {
                    'title': f"Laporan Keuangan Badan Informasi Geopasial {title.text.strip()}",
                    'url': title['href']
                }
                yield data

    def download(self):
        for data in self.get_data():
            file_name = data["title"].lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
            path_file = f's3://ai-pipeline-raw-data/data/data_descriptive/big/laporan_keuangan/pdf/{file_name}.pdf'
            json_file = f's3://ai-pipeline-raw-data/data/data_descriptive/big/laporan_keuangan/json/{file_name}.json'

            # Request file with streaming to handle large files
            response = requests.get(data['url'], stream=True)
            response.raise_for_status()  # Raise an error for bad responses

            # Save file using StorageManager
            StorageManager().save(path_file, response)
            print(f"File saved: {path_file}")

            metadata = {
                "link": data['url'],
                "tags": [
                    "badan_informasi_geopasial",
                    "laporan_keuangan"
                ],
                "source": "big.go.id",
                "title": data['title'],
                "sub_title": None,
                "range_data": data['title'].split(" ")[-1],
                "create_date": None,
                "update_date": None,
                "desc": None,
                "category": "Laporan Keuangan",
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
            print(f"Metadata saved: {json_file}")