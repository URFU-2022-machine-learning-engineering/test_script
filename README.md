#Audio File Sender

This repository contains a Python script that sends audio files from a specified directory to a given endpoint using asynchronous HTTP requests. The script utilizes aiohttp for handling asynchronous HTTP operations and aiofiles for asynchronous file handling. Additionally, the script incorporates tqdm for progress display and Poetry for dependency management.
Features

- Asynchronously sends audio files to a specified endpoint.
- Supports multiple audio file formats: MP3, WAV, AAC, and OPUS.
- Sends additional random files during specific times of the day (morning and evening).
- Displays progress using tqdm.

## Requirements

- Python 3.7+
- Poetry for dependency management

## Installation

1. Clone the repository:

```sh

git clone https://github.com/yourusername/audio-file-sender.git
cd audio-file-sender
```
2. Install dependencies using Poetry:

```sh

poetry install
```
## Usage

1. Run the script:

```sh
poetry run python audio_file_sender.py
```
2. Follow the prompts to enter the endpoint and the path to your audio folder.

## Script Details
### Main Function

```python
if __name__ == "__main__":
    ENDPOINT = input("Please enter the endpoint: ")
    directory = input("Please enter the path to your audio folder: ")
    asyncio.run(send_audio_files(directory, ENDPOINT))
```
### Functions
- send_file(session, endpoint, file_name, file_content_path): Sends a single file to the specified endpoint.
- send_random_files(session, endpoint, audio_files, count, sleep_range): Sends a specified number of random files with a random sleep interval between sends.
- send_audio_files(directory, endpoint): Main function that iterates over audio files in the directory and sends them.
- find_audio_files(directory): Generator that finds audio files with supported extensions in the specified directory.

### Asynchronous Handling

The script uses aiohttp for making asynchronous HTTP requests and aiofiles for non-blocking file operations. This ensures efficient handling of multiple file uploads.
### Time-Based Logic

- Morning (8 AM to 12 PM): Sends 7 additional random files.
- Evening (6 PM to 8 PM): Sends 5 additional random files.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

- The aiohttp library for asynchronous HTTP requests.
- The aiofiles library for asynchronous file handling.
- The tqdm library for progress bars.

For any issues or questions, please open an issue on GitHub.
