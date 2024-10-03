from datetime import datetime
import json
import time
import requests
from src.lib.storage_manager import StorageManager

headers = {
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://mori-m-foundation.or.jp/english/ius2/gpci2/',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"',
}

response = requests.get('https://mori-m-foundation.or.jp/ius/gpci/json/gpci2023_en.json', headers=headers)
datas = response.json()

for data in datas:
    file_name = data["City Name"].lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
    file_path = f's3://ai-pipeline-raw-data/data/data_statistics/globalpowercityidex/gpci/json/{file_name}.json'

    metadata = {
        "link": "https://mori-m-foundation.or.jp/english/ius2/gpci2/",
        "tags": [
            "global_power_city_index",
            "gpci"
        ],
        "source": "mori-m-foundation.or.jp",
        "title": data['City Name'],
        "sub_title": None,
        "range_data": None,
        "create_date": None,
        "update_date": None,
        "desc": None,
        "category": "GPCI",
        "sub_category": None,
        "data": data,
        "path_data_raw": [
            file_path
        ],
        "crawling_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "crawling_time_epoch": int(time.time()),
        "table_name": "judul_tabel",
        "country_name": "Indonesia",
        "level": "Nasional",
        "stage": "Crawling data",
        "update_schedule": "yearly"
    }   
    StorageManager().save_json(file_path, json.dumps(metadata))
    print(json.dumps(metadata))