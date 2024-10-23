import yt_dlp
import tkinter as tk
from tkinter import messagebox

def download_video(url, format_choice):
    if format_choice == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif format_choice == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
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

def start_download():
    video_url = url_entry.get()
    format_choice = format_var.get()
    download_video(video_url, format_choice)

# Create the main window
root = tk.Tk()
root.title("Video Downloader")

# Create and place the URL label and entry
url_label = tk.Label(root, text="Enter video URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create and place the format selection radio buttons
format_var = tk.StringVar(value='mp3')  # Default format
mp3_radio = tk.Radiobutton(root, text="mp3", variable=format_var, value='mp3')
mp4_radio = tk.Radiobutton(root, text="mp4", variable=format_var, value='mp4')
mp3_radio.pack(pady=5)
mp4_radio.pack(pady=5)

# Create and place the download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack(pady=20)

# Run the application
root.mainloop()
