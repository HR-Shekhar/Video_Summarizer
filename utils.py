def get_youtube_video_id(url: str) -> str:
    try:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        if "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
    except:
        pass
    return None

