import os
import requests
from tqdm import tqdm
import glob
import random
import time
from datetime import datetime


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


def send_random_file(audio_files, endpoint):
    if audio_files:
        random_file = random.choice(audio_files)
        file_name = os.path.basename(random_file)
        send_file(endpoint, file_name, random_file)


def send_audio_files(directory: str, endpoint: str):
    audio_files = list(find_audio_files(directory))
    if not audio_files:
        print("No audio files found in the specified directory.")
        return

    for audio_file in tqdm(audio_files, desc="Sending audio files"):
        file_name = os.path.basename(audio_file)
        send_file(endpoint, file_name, audio_file)

        current_hour = datetime.now().hour
        if 8 <= current_hour < 12:  # Morning
            print("Morning time")
            time.sleep(random.randint(1, 5))  # More frequent requests in the morning
            send_random_file(audio_files, endpoint)  # Send an additional random file
        elif 12 <= current_hour < 18:  # Day time (excluding morning and evening)
            print("Day time")
            time.sleep(random.randint(6, 10))
        elif 18 <= current_hour < 20:  # Evening
            print("Evening time")
            time.sleep(random.randint(2, 7))  # More frequent requests in the evening
            send_random_file(audio_files, endpoint)  # Send an additional random file
        else:  # Night time
            print("Night time")
            time.sleep(random.randint(11, 15))  # Less frequent requests at night


if __name__ == "__main__":
    ENDPOINT = "https://api.dzailz.su/upload"
    directory = input("Please enter the path to your audio folder: ")
    send_audio_files(directory, ENDPOINT)
