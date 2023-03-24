from dotenv import find_dotenv, load_dotenv
import os, json


# INITIALIZING ENV VARIABLE TO MAKE ACCESSIBLE TO WHOLE APPLICATION
def env_var_config():
    # finding env file location / path
    dotenv_path = find_dotenv()

    # loading environment variables
    load_dotenv(dotenv_path)

    # returning env variables by converting in json
    env_variables = {
        "upload": os.getenv("ASSEMBLY_UPLOAD_URL"),
        "transcribe": os.getenv("ASSEMBLY_TRANSCRIBE_URL"),
        "api_key": os.getenv("ASSEMBLY_API_KEY"),
    }

    return env_variables
