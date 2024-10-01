from src.controller.badan_informasi_geopasial.laporan_keuangan import LaporanKeuangan
from src.controller.badan_informasi_geopasial.laporan_kinerja import LaporanKinerja
from src.controller.mpr.majalah import Majalah
from src.controller.sipukat.rtsp import Rtsp
from src.controller.sipukat.hpl import Hpl
import argparse

def main(class_name, url, total_pages):
    if class_name == "Majalah":
        downloader = Majalah(url, total_pages)
        downloader.download()

    elif class_name == "hpl":
        hpl = Hpl()
        hpl.process()

    elif class_name == "rtsp":
        rtsp = Rtsp()
        rtsp.process()

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download file using specified class.")
    parser.add_argument("-n", "--name", type=str, required=True, help="Nama class yang ingin digunakan.")
    parser.add_argument("-u", "--url", type=str, required=False, help="Base URL untuk publikasi.")
    parser.add_argument("-p", "--page", type=int, required=False, help="Jumlah halaman yang ingin didownload.")

    args = parser.parse_args()
    main(args.name, args.url, args.page)