import yt_dlp
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import re

def download_video(url, format_choice, progress_label, progress_bar):
        
    def progress_hook(d):
        if d['status'] == 'downloading':
            raw_downloaded = d.get('_percent_str', '0%')
            downloaded = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', raw_downloaded).strip()

            try:
                progress_value = float(downloaded.strip('%'))
            except ValueError:
                progress_value = 0.0

            speed = d.get('_speed_str', 'N/A')
            eta = d.get('eta', 'N/A')

            progress_label.config(text=f"Pobieranie: {downloaded} | Szybkość: {speed} | ETA: {eta}s")
            progress_bar['value'] = progress_value
            root.update_idletasks() 
    
    if format_choice == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook],
        }
    elif format_choice == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }
    else:
        messagebox.showerror("Error", "Invalid format choice. Please select 'mp3' or 'mp4'.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            messagebox.showinfo("Success", f"Downloaded: {video_title}")
        except yt_dlp.DownloadError as e:
            messagebox.showerror("Download Error", str(e))
        finally:
            # Reset pola URL i paska postępu
            url_entry.delete(0, tk.END)
            progress_label.config(text="Postęp: 0%")
            progress_bar['value'] = 0

def start_download():
    video_url = url_entry.get()
    format_choice = format_var.get()

    if not video_url.strip():
        messagebox.showerror("Error", "URL cannot be empty.")
        return

    download_thread = threading.Thread(target=download_video, args=(video_url, format_choice, progress_label, progress_bar))
    download_thread.start()

# Create the main window
root = tk.Tk()
root.title("YT Downloader")

# Create and place the URL label and entry
url_label = tk.Label(root, text="Enter URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create and place the format selection radio buttons
format_var = tk.StringVar(value='mp3')
mp3_radio = tk.Radiobutton(root, text="mp3", variable=format_var, value='mp3')
mp4_radio = tk.Radiobutton(root, text="mp4", variable=format_var, value='mp4')
mp3_radio.pack(pady=5)
mp4_radio.pack(pady=5)

# Create and place the progress label
progress_label = tk.Label(root, text="Postęp: 0%")
progress_label.pack(pady=5)

# Create and place the progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

# Create and place the download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack(pady=20)

# Run the application
root.mainloop()
