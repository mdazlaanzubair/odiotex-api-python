from pytube import YouTube
import os


# FUNCTION TO DOWNLOAD YOUTUBE VIDEO AND SAVE IT IN AUDIO FILE
def yt_video_download(video_url, user):
    # fetching youtube content from the requested url
    video = YouTube(video_url)

    # filtering out best audio format to downloading for transcribing
    audio_stream = video.streams.filter(only_audio=True) 
    audio_file = audio_stream[-1].download()

    # renaming file with the username so that every time user transcribe 
    # new video it will be replaced with the previous one to save storage 
    os.rename(audio_file, f"audios/{user}_audio.mp3")

    # creating data dictionary to hold youtube content meta info
    video_meta_data = {
        "title": video.title,
        "desc": video.description,
        "duration": video.length,
        "thumb_img": video.thumbnail_url,
        "publish_on": video.publish_date.isoformat(),
        "tags": video.keywords,
        "views": video.views,
        "owner": video.author,
        "channel": video.channel_url,
        # returning audio file name so that on transcribing request same 
        # can be accessed from the storage
        "saved_audio_file": f"{user}_audio.mp3",
    }

    # returning the data
    return video_meta_data