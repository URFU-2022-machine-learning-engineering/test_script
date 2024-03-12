import os
import random
import asyncio
import aiohttp
import aiofiles
from tqdm.asyncio import tqdm
import glob


async def send_file(session, endpoint, file_name, file_content):
    data = aiohttp.FormData()
    data.add_field('file', file_content, filename=file_name, content_type='application/octet-stream')

    async with session.post(endpoint, data=data) as response:
        if response.status == 200:
            text = await response.text()
            print(f"Success! File {file_name} sent. Response: {text}")
        else:
            print(
                f"Failed to send the file {file_name}. Status code: {response.status}, Response: {await response.text()}")


async def find_and_send_audio_files(directory: str, endpoint: str):
    audio_extensions = ['*.mp3', '*.wav', '*.aac', '*.opus']
    audio_files = [os.path.join(root, file)
                   for root, _, files in os.walk(directory)
                   for extension in audio_extensions
                   for file in glob.glob1(root, extension)]

    if not audio_files:
        print("No audio files found in the specified directory.")
        return

    async with aiohttp.ClientSession() as session:
        tasks = []
        for audio_file in tqdm(audio_files, desc="Sending audio files"):
            print(f"Sending file {audio_file}")
            task = asyncio.create_task(send_audio_file(session, endpoint, audio_file))
            tasks.append(task)
            await asyncio.sleep(random.uniform(0.5, 1.5))  # Throttle requests
        await asyncio.gather(*tasks)


async def send_audio_file(session, endpoint, audio_file):
    try:
        async with aiofiles.open(audio_file, 'rb') as file_content:
            data = await file_content.read()
            await send_file(session, endpoint, os.path.basename(audio_file), data)
    except OSError as e:
        print(f"Error opening file {audio_file}: {e}")


if __name__ == "__main__":
    ENDPOINT = "https://api.dzailz.su/upload"
    directory = input("Please enter the path to your audio folder: ")
    asyncio.run(find_and_send_audio_files(directory, ENDPOINT))
