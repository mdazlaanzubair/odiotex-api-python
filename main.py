from flask import Flask, jsonify, request
from pytube import YouTube
import os
import requests
from dotenv import find_dotenv, load_dotenv

# initializing Flask app
app = Flask(__name__)

# finding env file location / path
dotenv_path = find_dotenv()

# loading environment variables
load_dotenv(dotenv_path)

# route to find youtube video from requested url and download 
# its audio for transcribing
@app.route("/download", methods=["POST"])
def grab_yt_video():
    # getting data from request
    req_url = request.get_json()['url']
    user = request.get_json()['user']

    # fetching youtube content from the link
    video = YouTube(req_url)
    # downloading audio track of video for transcribing
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

    # sending data to client
    return jsonify(video_meta_data)

# route to transcribe the requested video
@app.route("/transcribe", methods=["POST"])
def transcribe():
    # getting data from request
    req_file = request.get_json()['audio_file']

    # catching environment variables
    assembly_ai = {
        "upload": os.getenv("ASSEMBLY_UPLOAD_URL"),
        "transcribe": os.getenv("ASSEMBLY_TRANSCRIBE_URL"),
        "key": os.getenv("ASSEMBLY_API_KEY")
    }

    return req_file

if __name__ == "__main__":
    app.run(debug=True)