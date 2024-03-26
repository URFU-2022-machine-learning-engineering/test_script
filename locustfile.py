from locust import HttpUser, task, between, TaskSet
import os
import random
import glob


def find_audio_files(directory: str):
    audio_extensions = ['*.mp3', '*.wav', '*.aac', '*.opus']
    audio_files = []
    for root, _, _ in os.walk(directory):
        for extension in audio_extensions:
            for audio_file in glob.glob(os.path.join(root, extension)):
                audio_files.append(audio_file)
    return audio_files


class UploadBehavior(TaskSet):
    directory = "/home/dzailz/Downloads/golos_opus"  # Change this to your directory
    audio_files = find_audio_files(directory)

    @task
    def send_file(self):
        if not self.audio_files:
            print("No audio files found in the specified directory.")
            return

        audio_file = random.choice(self.audio_files)
        file_name = os.path.basename(audio_file)

        with open(audio_file, 'rb') as file:
            files = {'file': (file_name, file)}
            response = self.client.post("/upload", files=files)
            if response.status_code == 200:
                print(f"Success! File {file_name} sent.")
            else:
                print(f"Failed to send the file {file_name}. Status code: {response.status_code}")


class WebsiteUser(HttpUser):
    tasks = [UploadBehavior]
    wait_time = between(1, 3)

    def on_start(self):
        """ Any tasks to run before the load test starts """
        pass

    def on_stop(self):
        """ Any tasks to run after the load test ends """
        pass
