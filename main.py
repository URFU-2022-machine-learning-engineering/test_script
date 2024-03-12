import os
import requests
from tqdm import tqdm
import glob
import random
import time


def send_file(endpoint, file_name, file_content):
    files = {'file': (open(file_content, 'rb'))}
    try:
        response = requests.post(endpoint, files=files)
        if response.status_code == 200:
            print(f"Success! File {file_name} sent. Response: {response.text}")
        else:
            print(f"Failed to send the file {file_name}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed for file {file_name}: {e}")
    finally:
        files['file'].close()


def find_audio_files(directory: str):
    audio_extensions = ['*.mp3', '*.wav', '*.aac', '*.opus']
    for root, _, _ in os.walk(directory):
        for extension in audio_extensions:
            for audio_file in glob.glob(os.path.join(root, extension)):
                yield audio_file


def send_audio_files(directory: str, endpoint: str):
    audio_files = list(find_audio_files(directory))
    if not audio_files:
        print("No audio files found in the specified directory.")
        return

    for audio_file in tqdm(audio_files, desc="Sending audio files"):
        file_name = os.path.basename(audio_file)
        send_file(endpoint, file_name, audio_file)
        time.sleep(random.randint(1, 13))  # Simulate network or processing delays


if __name__ == "__main__":
    ENDPOINT = "https://api.dzailz.su/upload"
    directory = input("Please enter the path to your audio folder: ")
    send_audio_files(directory, ENDPOINT)
