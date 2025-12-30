import requests
import certifi

class DownloadWorker:
    def __init__(self, url, start, end, filename, progress_callback=None):
        self.url = url
        self.start = start
        self.end = end
        self.filename = filename
        self.progress_callback = progress_callback  # callback pour la progression

    def download(self):
        headers = {"Range": f"bytes={self.start}-{self.end}"}
        r = requests.get(self.url, headers=headers, stream=True, verify=certifi.where())
        with open(self.filename, "r+b") as f:
            f.seek(self.start)
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    if self.progress_callback:
                        self.progress_callback(len(chunk))
            f.flush()
