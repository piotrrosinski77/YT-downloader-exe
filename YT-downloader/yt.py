import yt_dlp

def download_video(url, format_choice):
    if format_choice == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',  # najlepsze dostępne audio
            'outtmpl': '%(title)s.%(ext)s',  # nazwa pliku wynikowego
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif format_choice == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # najlepsze dostępne video i audio
            'outtmpl': '%(title)s.%(ext)s',  # nazwa pliku wynikowego
        }
    else:
        print("Nieprawidłowy wybór formatu. Wybierz 'mp3' lub 'mp4'.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            print(f"Pobrano: {video_title}")
        except yt_dlp.DownloadError as e:
            print(f"Błąd podczas pobierania: {e}")

if __name__ == "__main__":
    video_url = input("Podaj URL filmu do pobrania: ")
    format_choice = input("Wybierz format (mp3 lub mp4): ").lower()
    download_video(video_url, format_choice)
