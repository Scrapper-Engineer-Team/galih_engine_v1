import json
import re
from bs4 import BeautifulSoup
from loguru import logger
import requests
import greenstalk
import concurrent.futures

code_provs = [
    12, 13, 14, 15, 16, 18, 33, 
    35,
      36, 17, 32, 51, 52, 53, 61, 62, 63, 64, 65, 71, 72, 73, 74, 34, 21, 19, 75, 76, 82, 11, 81, 31, 91, 95, 93, 94, 96, 92
]
# years = [
#     # '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', 
#     # '2021', 
#     # '2022', '2023',
#      '2024'
# ]
jenis_wikera = [
    "TORA",
      "PIAPS", "HA", "PPPBM"
]
tahapans = [
    "T1", 
    "T2", "T3", "T4", "T5", "T6", "T7", "T8"
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

    def clean_text(self, text):
        if isinstance(text, str):
            # Menghapus karakter whitespace ekstra dan menghilangkan karakter non-printable
            text = re.sub(r'\s+', ' ', text)  # Mengganti beberapa spasi dengan satu spasi
            text = text.strip()  # Menghapus spasi di awal dan akhir
            text = re.sub(r'[^\x20-\x7E]', '', text)  # Menghapus karakter non-printable
        return text

    def fetch_links(self, provs, jewi, tahapan):
        data_found = False
        for i in range(0, 201, 10):
            params = {
                'tipe': '1',
                'tahun': '2024',
                'mmode': '0',
                'bulan': '12',
                'kd_prop': provs,
                'jenis_wikera': jewi,
                'kode_tahapan': tahapan,
            }

            url = f'https://tanahkita.id/data/wilayah_kelola/index/{i}'
            logger.info(f"Fetching URL: {url} with params: {params}")

            try:
                response = requests.get(url, params=params, cookies=self.cookies, headers=self.headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.select('td a')
                profs = soup.select('tr td[align="justify"]')
                years = soup.select('tr td:nth-child(2)')
                tahaps = soup.select('tr td:nth-child(6)')

                if links:
                    data_found = True
                    for link, prof, year, tahapnya in zip(links, profs, years, tahaps):
                        href = link.get('href')
                        profile = prof.text.strip()

                        if href:
                            full_link = requests.compat.urljoin(response.url, href)
                            base_meta = {
                                'kd_prop': provs,
                                'profile': self.clean_text(profile) if profile else None,
                                'jenis_wikera': jewi,
                                'tahun': year.text.strip().split('-')[-1] if year else None,
                                'url': full_link,
                                'tahap': tahapnya.text.strip()
                            }
                            client = greenstalk.Client(('192.168.99.69', 11300), use='sc-tanah-kita-baselink')
                            client.put(json.dumps(base_meta), ttr=3600)
                else:
                    # If no links found, we've reached the end of the data
                    break

            except requests.HTTPError as http_err:
                logger.error(f"HTTP error occurred: {http_err} for URL: {url}")
                break
            except Exception as err:
                logger.error(f"Other error occurred: {err} for URL: {url}")
                break

        return data_found

    def get_link(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            for provs in code_provs:
                # for year in years:
                for jewi in jenis_wikera:
                    for tahapan in tahapans:
                        futures.append(executor.submit(self.fetch_links, provs, jewi, tahapan))

            # Wait for all futures to complete and check for data found
            for future in concurrent.futures.as_completed(futures):
                if not future.result():
                    logger.info("Continuing to the next tahapan or province.")

    def process(self):
        self.get_link()