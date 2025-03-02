import yt_dlp

def download_instagram_media(url):
    """Instagramdan video yoki rasm yuklab oladi."""
    ydl_opts = {
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

            # 🔍 Media turini to‘g‘ri aniqlash
            if 'entries' in info:
                info = info['entries'][0]  # Agar playlist yoki ko‘p media bo‘lsa
            if 'ext' in info and info['ext'] in ['mp4', 'webm', 'mov']:
                media_type = "video"
            else:
                media_type = "photo"

            return file_path, media_type
        except Exception as e:
            print("Yuklashda xatolik:", e)
            return None, None
