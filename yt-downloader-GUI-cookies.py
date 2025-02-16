import yt_dlp
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import re
import os
from PIL import Image, ImageTk

# TO-DO:
# - Add fancy font
# - Resize the background image to fit the window
# - Add a button to stop downloading process


def download_video(url, format_choice, progress_label, progress_bar):

    def progress_hook(d):
        if d["status"] == "downloading":
            raw_downloaded = d.get("_percent_str", "0%")
            downloaded = re.sub(
                r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", raw_downloaded
            ).strip()

            try:
                progress_value = float(downloaded.strip("%"))
            except ValueError:
                progress_value = 0.0

            speed = d.get("_speed_str", "N/A")
            eta = d.get("eta", "N/A")

            progress_label.config(
                text=f"Downloading: {downloaded} | Speed: {speed} | ETA: {eta}s"
            )
            progress_bar["value"] = progress_value
            root.update_idletasks()

    cookies_file = "cookies.txt" if os.path.exists("cookies.txt") else None

    if format_choice == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "progress_hooks": [progress_hook],
            "cookies": cookies_file,
        }
    elif format_choice == "mp4":
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "progress_hooks": [progress_hook],
            "cookies": cookies_file,
        }
    else:
        messagebox.showerror(
            "Error", "Invalid format choice. Please select 'mp3' or 'mp4'."
        )
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get("title", "video")
            messagebox.showinfo("Success", f"Downloaded: {video_title}")
        except yt_dlp.DownloadError as e:
            messagebox.showerror("Download Error", str(e))
        finally:
            url_entry.delete(0, tk.END)
            progress_label.config(text="Progress: 0%")
            progress_bar["value"] = 0


def start_download():
    video_url = url_entry.get()
    format_choice = format_var.get()

    if not video_url.strip():
        messagebox.showerror("Error", "URL cannot be empty.")
        return

    download_thread = threading.Thread(
        target=download_video,
        args=(video_url, format_choice, progress_label, progress_bar),
    )
    download_thread.start()


root = tk.Tk()
root.title("YT Downloader")
root.geometry("500x275")

background_image = Image.open("bg.jpg")
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

url_label = tk.Label(root, bg="#99494C", width=444, text="Enter URL from YouTube:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

format_var = tk.StringVar(value="mp3")
mp3_radio = tk.Radiobutton(
    root, bg="#99494C", text="mp3", variable=format_var, value="mp3"
)
mp4_radio = tk.Radiobutton(
    root, bg="#99494C", text="mp4", variable=format_var, value="mp4"
)
mp3_radio.pack(pady=5)
mp4_radio.pack(pady=5)

progress_label = tk.Label(root, bg="#99494C", text="Progess: 0%")
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(
    root, orient="horizontal", length=444, mode="determinate"
)
progress_bar.pack(pady=5)

photo = tk.PhotoImage(file="button4.png")

download_button = tk.Button(
    root,
    image=photo,
    text="Download",
    font=("Arial", 12),
    width=186,
    height=29,
    command=start_download,
)

download_button.pack(pady=20)

root.mainloop()
