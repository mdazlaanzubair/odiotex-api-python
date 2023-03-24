import requests, json
from time import sleep

# CUSTOM HELPER MODULES
from helpers.fileFunc import find_file, read_file


# FUNCTION THAT TAKES AND UPLOAD AUDIO FILE TO THE SERVER FOR TRANSCRIPTION
def uploadFile(file_path, api_key, upload_endpoint):
    # file exist start uploading
    if file_path:
        # preparing header
        auth_header = {"authorization": api_key}

        # uploading file
        upload_file_url = requests.post(
            upload_endpoint, headers=auth_header, data=read_file(file_path)
        )

        # returning upload url on successful upload
        return {"status": True, "url": upload_file_url.json()["upload_url"]}
    else:
        return {"status": False}


# FUNCTION THAT TAKES URL OF UPLOADED AUDIO FILE AND STARTS TRANSCRIBING
def transcribeFile(upload_url, api_key, transcribe_endpoint):
    # First - creating transcribe request payload and headers
    transcript_request = {
        "audio_url": upload_url,
        "iab_categories": True,
    }

    # Second - preparing header
    req_header = {"authorization": api_key, "content-type": "application/json"}

    # Third - requesting for transcription
    transcript_response = requests.post(
        transcribe_endpoint, json=transcript_request, headers=req_header
    )

    # Fourth - returning response
    return transcript_response.json()["id"]


# FUNCTION THAT TAKE TRANSCRIPTION ID AND CHECK THE TRANSCRIPTION IS DONE OR OTHERWISE
def checkTranscription(transcript_id, api_key, transcribe_endpoint):
    # First - creating endpoint that check the transcription status
    checking_endpoint = transcribe_endpoint + "/" + transcript_id

    # Second - preparing header
    req_header = {"authorization": api_key, "content-type": "application/json"}

    # Third - requesting for transcription status
    check_trans_res = requests.get(checking_endpoint, headers=req_header)

    # Fourth - request for transcription after every 30s until the status is "completed"
    while check_trans_res.json()["status"] != "completed":
        # sleep time before every request
        sleep(35)

        # using try / catch block to catch any exceptions that may occur when attempting
        # to send a GET request to the server.
        try:
            check_trans_res = requests.get(checking_endpoint, headers=req_header)
        except:
            return check_trans_res.json()["status"]

    # Fifth - once transcription is completed, return the transcription text
    return check_trans_res.json()["text"]
