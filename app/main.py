import tkinter as tk
from tkinter import ttk, messagebox
import threading
from downloader.manager import DownloadManager
import os
from urllib.parse import urlparse
import time

class ModernDownloaderApp:
    def __init__(self, root):
        self.root = root
        root.title("Kachow !!")
        root.geometry("550x380")
        root.resizable(False, False)
        root.configure(bg="#2b2b2b")

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", thickness=25, troughcolor="#444444", background="#00bfff")
        
        tk.Label(root, text="URL du fichier:", bg="#2b2b2b", fg="white", font=("Arial", 11)).pack(anchor='w', padx=15, pady=(15,0))
        self.url_entry = tk.Entry(root, width=60, font=("Arial", 11))
        self.url_entry.pack(padx=15, pady=5, fill='x')

        tk.Label(root, text="Nom du fichier (optionnel):", bg="#2b2b2b", fg="white", font=("Arial", 11)).pack(anchor='w', padx=15, pady=(10,0))
        self.name_entry = tk.Entry(root, width=60, font=("Arial", 11))
        self.name_entry.pack(padx=15, pady=5, fill='x')

        tk.Label(root, text="Nombre de threads:", bg="#2b2b2b", fg="white", font=("Arial", 11)).pack(anchor='w', padx=15, pady=(10,0))
        self.thread_entry = tk.Entry(root, width=10, font=("Arial", 11))
        self.thread_entry.insert(0, "4")
        self.thread_entry.pack(anchor='w', padx=15, pady=5)

        self.progress = ttk.Progressbar(root, length=500, mode='determinate')
        self.progress.pack(pady=20)

        self.percent_label = tk.Label(root, text="0%", bg="#2b2b2b", fg="white", font=("Arial", 11))
        self.percent_label.pack()
        self.time_label = tk.Label(root, text="Temps écoulé: 0s", bg="#2b2b2b", fg="white", font=("Arial", 11))
        self.time_label.pack()

        self.download_btn = tk.Button(root, text="Kachow !!", command=self.start_download,
                                      bg="#00bfff", fg="white", font=("Arial", 12, "bold"),
                                      activebackground="#009acd", relief="flat", padx=10, pady=5)
        self.download_btn.pack(pady=15)

    def get_filename(self, url, custom_name=None):
        parsed = urlparse(url)
        orig_name = os.path.basename(parsed.path)
        ext = os.path.splitext(orig_name)[1]

        if custom_name:
            if not os.path.splitext(custom_name)[1] and ext:
                return custom_name + ext
            return custom_name
        else:
            return orig_name or "downloaded_file.bin"

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Attention", "Veuillez entrer une URL")
            return

        try:
            threads = int(self.thread_entry.get())
            if threads < 1:
                threads = 4
        except:
            threads = 4

        threading.Thread(target=self.download_file, args=(url, threads), daemon=True).start()

    def download_file(self, url, threads):
        start_time = time.time()
        custom_name = self.name_entry.get().strip()
        filename = self.get_filename(url, custom_name)

        def progress_callback(downloaded_bytes, total_size):
            percent = int(downloaded_bytes / total_size * 100)
            self.progress['value'] = percent
            self.percent_label.config(text=f"{percent}%")

            elapsed = int(time.time() - start_time)
            speed = downloaded_bytes / elapsed if elapsed > 0 else 0
            remaining = int((total_size - downloaded_bytes) / speed) if speed > 0 else 0
            self.time_label.config(text=f"Temps écoulé: {elapsed}s | Temps restant: {remaining}s")

        manager = DownloadManager()
        try:
            manager.download(url, filename, parts=threads, progress_callback=progress_callback)
            self.progress['value'] = 100
            self.percent_label.config(text="100%")
            self.time_label.config(text=f"Terminé en {int(time.time() - start_time)}s")
            messagebox.showinfo("Kachow !!", f"Téléchargement terminé!\nFichier: {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDownloaderApp(root)
    root.mainloop()
