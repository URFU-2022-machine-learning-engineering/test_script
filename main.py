import os
import aiohttp
import asyncio
from aiohttp import FormData
from tqdm.asyncio import tqdm_asyncio as tqdm
import glob
import random
from datetime import datetime
import aiofiles


async def send_file(session, endpoint, file_name, file_content_path):
    async with aiofiles.open(file_content_path, 'rb') as file:
        data = FormData()
        data.add_field('file', await file.read(), filename=file_name)
        try:
            async with session.post(endpoint, data=data) as response:
                if response.status == 200:
                    print(f"Success! File {file_name} sent. Response: {await response.text()}")
                else:
                    print(f"Failed to send the file {file_name}. Status code: {response.status}")
        except aiohttp.ClientError as e:
            print(f"Request failed for file {file_name}: {e}")


async def send_random_files(session, endpoint, audio_files, count, sleep_range):
    for _ in range(count):
        random_file = random.choice(audio_files)
        file_name = os.path.basename(random_file)
        await send_file(session, endpoint, file_name, random_file)
        await asyncio.sleep(random.randint(*sleep_range))


async def send_audio_files(directory: str, endpoint: str):
    audio_files = [audio_file for audio_file in find_audio_files(directory)]
    if not audio_files:
        print("No audio files found in the specified directory.")
        return

    async with aiohttp.ClientSession() as session:
        for audio_file in tqdm(audio_files, desc="Sending audio files"):
            file_name = os.path.basename(audio_file)
            await send_file(session, endpoint, file_name, audio_file)

            current_hour = datetime.now().hour
            if 8 <= current_hour < 12:  # Morning
                print("Sending + 3 random files (It's morning time!)")
                await send_random_files(session, endpoint, audio_files, 7, (1, 3))
            elif 18 <= current_hour < 20:  # Evening
                print("Sending + 2 random files (It's evening time!)")
                await send_random_files(session, endpoint, audio_files, 5, (2, 4))


def find_audio_files(directory: str):
    audio_extensions = ['*.mp3', '*.wav', '*.aac', '*.opus']
    for root, _, _ in os.walk(directory):
        for extension in audio_extensions:
            for audio_file in glob.glob(os.path.join(root, extension)):
                yield audio_file


if __name__ == "__main__":
    ENDPOINT = "https://api.dzailz.su/upload"
    directory = input("Please enter the path to your audio folder: ")
    asyncio.run(send_audio_files(directory, ENDPOINT))
