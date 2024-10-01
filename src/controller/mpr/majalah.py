from datetime import datetime
import json
import time
from src.lib.beautifulsoup_engine import Soup
from src.lib.storage_manager import StorageManager
from loguru import logger
import requests
import s3fs

s3 = s3fs.S3FileSystem(
    key='GLZG2JTWDFFSCQVE7TSQ',
    secret='VjTXOpbhGvYjDJDAt2PNgbxPKjYA4p4B7Btmm4Tw',
    client_kwargs={'endpoint_url': 'http://10.12.1.149:8000'}
)

class Majalah:
    def __init__(self, base_url, total_pages):
        self.base_url = base_url
        self.total_pages = total_pages  

    def get_data(self, page):
        url = f'{self.base_url}?page={page}'
        soup_instance = Soup(url)  
        
        if soup_instance.soup:  
            titles = soup_instance.select('center b')
            tautans = soup_instance.select('section.widget.widget_pearo_posts_thumb aside a')
            for title, tautan in zip(titles, tautans):
                data = {
                    'title': title.text.strip(),  
                    'url': tautan['href']
                }
                yield data
        else:
            logger.error(f'Error fetching data from {url}')

    def download_pdf(self, path_file, url):
        if url.startswith('/'):
            url = f'https://mpr.go.id{url}'

        urls_to_try = [
            url,
            f'https://mpr.go.id{url}',
        ]

        success = False
        for url_to_try in urls_to_try:
            try:
                response = requests.get(url_to_try)
                if response.status_code == 200:
                    StorageManager.save(path_file, response)  # Simpan langsung response
                    success = True
                    break
            except Exception as e:
                logger.error(f'Error saat mendownload dari {url_to_try}: {e}')

        if not success:
            logger.error(f'File tidak bisa didownload: {url}')
        
        return success

    def metadata(self, path_file, path_json, data):
        metadata = {
            "link": self.base_url,
            "tags": [
                "mpr",
                "publikasi",
                "majalah"
            ],
            "source": "mpr.go.id",
            "title": data["title"],
            "sub_title": "",
            "range_data": "",
            "create_date": "",
            "update_date": "",
            "desc": "",
            "category": "Publikasi",
            "sub_category": "Majalah",
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

        StorageManager.save_json(path_json, metadata)

    def download(self):
        for i in range(1, self.total_pages + 1):  
            datas = self.get_data(i)
            for data in datas:
                file_name = f'{data["title"].replace(" ", "_").replace("/", "_")}'
                path_file = f'test/mpr/majalah/{file_name}.pdf'
                path_json = f'test/mpr/majalah/{file_name}.json'

                if self.download_pdf(path_file, data["url"]):
                    self.metadata(path_file, path_json, data)
