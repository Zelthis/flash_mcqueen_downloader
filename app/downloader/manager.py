import os
from downloader.worker import DownloadWorker
from utils.network import get_file_info
import threading

class DownloadManager:
    def download(self, url, filename, parts=4, progress_callback=None):
        size, supports = get_file_info(url)
        print(f"Taille du fichier: {size} octets, supporte Range: {supports}")

        # Créer fichier vide
        with open(filename, "wb") as f:
            f.truncate(size)

        segment_size = size // parts
        threads = []

        # Progression partagée
        downloaded = [0]  # liste mutable pour callback

        def thread_progress(bytes_downloaded):
            downloaded[0] += bytes_downloaded
            if progress_callback:
                progress_callback(downloaded[0], size)

        for i in range(parts):
            start = i * segment_size
            end = size - 1 if i == parts - 1 else (start + segment_size - 1)
            worker = DownloadWorker(url, start, end, filename, progress_callback=thread_progress)
            t = threading.Thread(target=worker.download)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
        print("Téléchargement terminé")
