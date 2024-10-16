from loguru import logger
from src.controller.kpu.laporan_keuangan import LaporanKeuanganKpu
from src.controller.badan_informasi_geopasial.jurnal_ilmiah_geomatika import JurnalIlmiahGeomatika
from src.controller.badan_informasi_geopasial.laporan_keuangan import LaporanKeuangan
from src.controller.badan_informasi_geopasial.laporan_kinerja import LaporanKinerja
from src.controller.komisi_yudisial.infografis import InfografisKy
from src.controller.komisi_yudisial.laporan_keuangan import LaporanKeuanganKy
from src.controller.komisi_yudisial.year_book import YearBook
from src.controller.global_power_city_index.globalpowercityidex import GlobalPowerCityIndex
from src.controller.mpr.majalah import Majalah
from src.controller.tanah_kita.kelola_wilayah import KelolaWilayah
from src.controller.sipukat.hpl import Hpl
from src.controller.tanah_kita.pusher import PusherTakit
from src.controller.bank_indonesia.indicator import Indicator
from src.controller.bank_indonesia.download_excel import BIDownload
import argparse

def main(class_name, url, total_pages, tube):
    logger.success(f"Start process {class_name}...")
    if class_name == "Majalah":
        downloader = Majalah(url, total_pages)
        downloader.download()

    elif class_name == "hpl":
        hpl = Hpl()
        hpl.process()

    # elif class_name == "rtsp":
    #     rtsp = Rtsp()
    #     rtsp.process()

    elif class_name == "LaporanKinerja":
        if not url:
            print("Error: URL is required for LaporanKinerja")
            return
        laporan_kinerja = LaporanKinerja(url)
        laporan_kinerja.download()

    elif class_name == "LaporanKeuangan":
        if not url:
            print("Error: URL is required for LaporanKeuangan")
            return
        laporan_keuangan = LaporanKeuangan(url)
        laporan_keuangan.download()

    elif class_name == "JurnalIlmiahGeomatika":
        if not url:
            print("Error: URL is required for JurnalIlmiahGeomatika")
            return
        jurnal_ilmiah_geomatika = JurnalIlmiahGeomatika(url)
        jurnal_ilmiah_geomatika.process()
    
    elif class_name == "LaporanKeuanganKpu":
        laporan_keuangan_kpu = LaporanKeuanganKpu()
        laporan_keuangan_kpu.download()

    elif class_name == "InfografisKy":
        if not url:
            print("Error: URL is required for InfografisKy")
            return
        infografis_ky = InfografisKy(url)
        infografis_ky.download()

    elif class_name == "LaporanKeuanganKy":
        if not url:
            print("Error: URL is required for LaporanKeuanganKy")
            return
        laporan_keuangan_ky = LaporanKeuanganKy(url)
        laporan_keuangan_ky.process()

    elif class_name == "YearBook":
        if not url:
            print("Error: URL is required for YearBook")
            return
        year_book = YearBook(url)
        year_book.download()

    elif class_name == "GlobalPowerCityIndex":
        global_power_city_index = GlobalPowerCityIndex()
        global_power_city_index.download()

    elif class_name == "KelolaWilayah":
        kelola_wilayah = KelolaWilayah()
        kelola_wilayah.process()

    elif class_name == "PusherTakit":
        pusher = PusherTakit()
        pusher.process()

    elif class_name == "Indicator":
        indicator = Indicator()
        indicator.process()

    elif class_name == "BIDownload":
        indicator = Indicator()
        bi_download = BIDownload()

        for data in indicator.get_data():  # Iterasi setiap data yang di-yield
            if 'url' in data:
                download_url = data['url']
                title = data['title']
                value = data['value']
                date = data['date']
                logger.info(f"Downloading from: {download_url}")
                try:
                    bi_download.process(download_url, title, value, date)  # Proses download satu per satu
                except Exception as e:
                    logger.error(f"Failed to download from {download_url}: {e}")
    
    else:
        logger.error(f"Class {class_name} not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download file using specified class.")
    parser.add_argument("-n", "--name", type=str, required=True, help="Nama class yang ingin digunakan.")
    parser.add_argument("-u", "--url", type=str, required=False, help="Base URL untuk publikasi.")
    parser.add_argument("-p", "--page", type=int, required=False, help="Jumlah halaman yang ingin didownload.")
    parser.add_argument("-t", "--tube", type=str, required=False, help="Nama Tube yang diinginkan.")

    args = parser.parse_args()
    main(args.name, args.url, args.page, args.tube)