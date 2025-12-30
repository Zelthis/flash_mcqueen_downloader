import requests
import certifi

def get_file_info(url):
    """Retourne la taille totale et si le serveur supporte Range"""
    headers = {"Range": "bytes=0-0"}
    r = requests.get(url, headers=headers, stream=True, timeout=15, verify=certifi.where())
    
    content_range = r.headers.get("Content-Range")
    if content_range:
        total_size = int(content_range.split("/")[-1])
        return total_size, True

    content_length = r.headers.get("Content-Length")
    if content_length:
        total_size = int(content_length)
        return total_size, True

    raise Exception("Impossible de déterminer la taille du fichier")
