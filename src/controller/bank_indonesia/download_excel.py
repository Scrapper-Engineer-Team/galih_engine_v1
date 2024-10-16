from datetime import datetime
import json
import os
from loguru import logger
from playwright.sync_api import sync_playwright
from src.lib.storage_manager import StorageManager
import time
import s3fs

s3 = s3fs.S3FileSystem(
            key='GLZG2JTWDFFSCQVE7TSQ',
            secret='VjTXOpbhGvYjDJDAt2PNgbxPKjYA4p4B7Btmm4Tw',
            client_kwargs={'endpoint_url': f'http://10.12.1.149:8000'}
        )

class BIDownload:
    def process(self, download_url, title, value, date):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(download_url)

            # page.wait_for_load_state("networkidle")

            with page.expect_download() as download_info:
                page.get_by_role("button", name="Unduh").click()
            download = download_info.value

            download.save_as("data2.xlsx")

            time.sleep(5)
            
            file_name = title.replace(" ", "_").replace("/", "_")
            file_path = f's3://ai-pipeline-raw-data/data/data_statistics/Bank Indonesia/Indikator/excel/{file_name}.xlsx'
            json_path = f's3://ai-pipeline-raw-data/data/data_statistics/Bank Indonesia/Indikator/json/{file_name}.json'

            with open("data2.xlsx", "rb") as file:
                file_content = file.read()
            
            with s3.open(file_path, "wb") as f:
                f.write(file_content)
            logger.success(f'Saved Excel to s3 : {file_path}')

            os.remove("data2.xlsx")

            meatadata = {
                "link": download_url,
                "tags": [
                    "bank_indonesia",
                    "indicator"
                ],
                "source": "bi.go.id",
                "title": "​Indikator Moneter​​​​​​",
                "sub_title": "",
                "range_data": date.split(" ")[-1],
                "create_date": "",
                "update_date": "",
                "desc": "Indikator moneter menyediakan data/statistik moneter bulanan yang digunakan untuk mengetahui perkembangan besaran moneter secara ringkas dan cepat. Indikator moneter terdiri dari uang primer, posisi luar negeri bersih bank sentral, aktiva dalam negeri bersih bank sentral, serta cadangan devisa. Kebutuhan atas data/statistik serta uraian/penjelasan moneter lain tersedia pada Publikasi dan Statistik yang disajikan pada menu Publikasi dan menu Statistik.",
                "category": "Indicator",
                "sub_category": "",
                'data':{
                    "title": title,
                    "value": value,
                    "date": date
                },
                "path_data_raw": [
                    file_path,
                    json_path
                ],
                "crawling_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "crawling_time_epoch": int(time.time()),
                "table_name": "judul_tabel",
                "country_name": "Indonesia",
                "level": "Nasional",
                "stage": "Crawling data",
                "update_schedule": "monthly"
            }

            logger.success(json.dumps(meatadata))
            StorageManager().save_json(json_path, meatadata)