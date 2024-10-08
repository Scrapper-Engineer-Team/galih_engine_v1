import json
from bs4 import BeautifulSoup
from loguru import logger
import requests
from src.lib.storage_manager import StorageManager


code_provs = [
    12,13,14,15,16,18,33,35,36,17,32,51,52,53,61,62,63,64,65,71,72,73,74,34,21,19,75,76,82,11,81,31,91,95,93,94,96,92
]
years = [
    '1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024'
]
jenis_wikera = [
    "TORA","PIAPS","HA","PPPBM"
]
kode_tahapan = [
    'T1'
]

class PusherTakit:
    def __init__(self):
        self.cookies = {
            'PHPSESSID': 'g432p48nbh4fbohcvvj6k0tvp3',
            'lf_ci_session': 'a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%2209ac66c083b2ac3af3a8dec14ba33263%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22103.121.213.205%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A101%3A%22Mozilla%2F5.0+%28X11%3B+Linux+x86_64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F128.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1728282871%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D1cf06e2bc97f91cf065e130fa431c6de',
        }

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            # 'cookie': 'PHPSESSID=g432p48nbh4fbohcvvj6k0tvp3; lf_ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%2209ac66c083b2ac3af3a8dec14ba33263%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22103.121.213.205%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A101%3A%22Mozilla%2F5.0+%28X11%3B+Linux+x86_64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F128.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1728282871%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D1cf06e2bc97f91cf065e130fa431c6de',
            'priority': 'u=0, i',
            'referer': 'https://tanahkita.id/data/wilayah_kelola/?tipe=1&tahun=2024&mmode=0&kd_prop=&jenis_wikera=&kode_tahapan=',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }

        self.cookies2 = {
            'PHPSESSID': 'g432p48nbh4fbohcvvj6k0tvp3',
            'lf_ci_session': 'a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%224cc630c283cd8dfb562a4a02c820955e%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22103.121.213.205%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A101%3A%22Mozilla%2F5.0+%28X11%3B+Linux+x86_64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F128.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1728289904%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D4fb7cfc5dfaa8286b88a4b480a7ff283',
        }

        self.headers2 = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            # 'cookie': 'PHPSESSID=g432p48nbh4fbohcvvj6k0tvp3; lf_ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%224cc630c283cd8dfb562a4a02c820955e%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22103.121.213.205%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A101%3A%22Mozilla%2F5.0+%28X11%3B+Linux+x86_64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F128.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1728289904%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D4fb7cfc5dfaa8286b88a4b480a7ff283',
            'priority': 'u=0, i',
            'referer': 'https://tanahkita.id/data/wilayah_kelola/index/80?tipe=2&tahun=2023&mmode=1&bulan=12&kd_prop=&jenis_wikera=&kode_tahapan=',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36a',
        }


    def get_link(self, tube):
        for provs in code_provs:
            for year in years:
                for jewi in jenis_wikera:
                    for tahap in kode_tahapan:

                        # Variabel untuk mengecek apakah data ditemukan di halaman pertama
                        data_found_in_first_page = False

                        for i in range(0, 201):  # Loop untuk page index
                            params = {
                                'tipe': '2',
                                'tahun': year,
                                'mmode': '0',
                                'bulan': '12',
                                'kd_prop': provs,
                                'jenis_wikera': jewi,
                                'kode_tahapan': tahap,
                            }

                            url = f'https://tanahkita.id/data/wilayah_kelola/index/{i}'
                            logger.info(f"Fetching URL: {url} with params: {params}")

                            response = requests.get(
                                url,
                                params=params,
                                cookies=self.cookies2,
                                headers=self.headers2
                            )

                            # Cek jika request berhasil
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.text, 'html.parser')
                                links = soup.select('td a')  # Pilih elemen <a> di dalam elemen <td>

                                # Jika ada data ditemukan, ubah variabel menjadi True
                                if links:
                                    data_found_in_first_page = True

                                    # Loop untuk mengambil semua link yang ditemukan
                                    for link in links:
                                        href = link.get('href')
                                        if href:
                                            full_link = requests.compat.urljoin(response.url, href)
                                            
                                            base_meta = {
                                                'kd_prop': provs,
                                                'jenis_wikera': jewi,
                                                'kode_tahapan': tahap,
                                                'tahun': year,
                                                'url': full_link
                                            }

                                            StorageManager().send_beanstalk(base_meta, tube)
                                
                                # Jika loop pertama (`i == 0`) dan tidak ada data, break loop `i` dan lanjut ke kode tahapan berikutnya
                                elif i == 0 and not links:
                                    logger.error(f"No data found for first page of URL: {url}, skipping to next kode_tahapan.")
                                    break

                            else:
                                logger.error(f"Request failed for URL: {response.url} with status code: {response.status_code}")

                        # Jika tidak ada data ditemukan pada loop pertama (`i == 0`), lanjutkan ke tahapan berikutnya
                        if not data_found_in_first_page:
                            continue
                        
    def process(self, tube):
        self.get_link(tube)