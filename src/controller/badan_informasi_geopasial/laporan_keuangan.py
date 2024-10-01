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
            print(data)

    