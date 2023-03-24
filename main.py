from flask import Flask, jsonify, request
import os

# CUSTOM HELPER MODULES
from helpers.envConfig import env_var_config
from helpers.downloader import yt_video_download
from helpers.assemblyFuncs import uploadFile, transcribeFile, checkTranscription
from helpers.fileFunc import find_file


# INITIALIZING FLASK APP
app = Flask(__name__)


# INVOKING ENV VARIABLE
env_vars = env_var_config()


# GETTING AUDIO FILES DIRECTORY
# First - getting current working directory
cwd = os.getcwd()
# Second - appending "audios" to the current working directory
audio_dir = os.path.join(cwd, "audios")


# ROUTE TO DOWNLOAD YOUTUBE VIDEO AS AUDIO AND RETURN META DATA
@app.route("/download", methods=["POST"])
def grab_yt_video():
    # getting data from request
    req_url = request.get_json()["url"].strip()
    user = request.get_json()["user"]

    # calling download function to get video url content
    meta_data = yt_video_download(req_url, user)

    # sending data to client
    return jsonify(meta_data)


# ROUTE TO TRANSCRIBE AUDIO FILE
@app.route("/transcribe", methods=["POST"])
def transcribe():
    # getting data from request
    req_file = request.get_json()["audio_file"]

    # FINDING REQUESTED FILE IN THE AUDIO DIRECTORY
    file_path = find_file(req_file, audio_dir)

    # UPLOAD FILE TO ASSEMBLY AI FOR TRANSCRIBING
    upload_response = uploadFile(file_path, env_vars["api_key"], env_vars["upload"])

    # checking response
    if upload_response["status"] == True:
        upload_audio_url = upload_response["url"]

        # STARTING TRANSCRIPTION OF UPLOADED FILE
        transcript_id = transcribeFile(
            upload_audio_url, env_vars["api_key"], env_vars["transcribe"]
        )

        # CHECKING IF TRANSCRIPTION IS COMPLETED OR OTHERWISE
        transcript = checkTranscription(
            transcript_id, env_vars["api_key"], env_vars["transcribe"]
        )

        # returning transcript of the video
        return jsonify({"data": transcript})

    else:
        return jsonify({"msg": "File doesn't exist!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
