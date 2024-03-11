import os
import random
import time

from minio import Minio
from minio.error import S3Error
import requests


def send_random_file_from_bucket(bucket_name, endpoint, minio_url, access_key, secret_key):
    # Initialize the MinIO client
    minio_client = Minio(
        minio_url,
        access_key=access_key,
        secret_key=secret_key,
        secure=False  # Set to True if MinIO server is using TLS
    )

    try:
        # List all object names in the bucket
        objects = minio_client.list_objects(bucket_name)
        object_names = [obj.object_name for obj in objects]

        if not object_names:
            print("The bucket is empty.")
            return

        # Select a random object
        random_object_name = random.choice(object_names)
        print(f"Selected file: {random_object_name}")

        # Get the object
        response = minio_client.get_object(bucket_name, random_object_name)

        # Read the content of the object
        file_content = response.read()
        response.close()
        response.release_conn()

        # Send the file to the given endpoint
        # Assuming the endpoint expects a multipart/form-data request
        files = {'file': (random_object_name, file_content)}
        response = requests.post(endpoint, files=files)

        print(f"File sent. Status code: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            print(response.text)
        else:
            print("Failed to send the file.")

    except S3Error as exc:
        print("Error occurred:", exc)


def send_random_file_from_disk(path: str, endpoint: str):
    try:
        list_of_files = os.listdir(path)
    except OSError:
        print("Failed to open path")
        return

    file_to_send = random.choice(list_of_files)
    print(f"Selected file: {file_to_send}")
    try:
        with open(path + "/" + file_to_send, 'rb') as file_content:
            files = {'file': (file_to_send, file_content)}
            response = requests.post(endpoint, files=files)
            assert response, "Response is empty"
    except OSError:
        print("Failed to open file")
    if response.status_code == 200:
        print("Success!")
        print(response.text)
    else:
        print("Failed to send the file.")


# Example usage
if __name__ == "__main__":
    ENDPOINT = "https://api.dzailz.su/upload"
    # ENDPOINT = "http://127.0.0.1:8787/upload"

    def run_minio():
        start_time = time.time()
        bucket_name = "audio"

        minio_url = "192.168.111.66:9000"
        access_key = "1T6fmN8xttey1SG4TXvd"
        secret_key = "PHFlySjbBJv1I21qjVgI0MD2VfcvxsC4tpKLFTtX"
        # Start timing

        time.sleep(random.randint(1, 22))
        send_random_file_from_bucket(bucket_name, ENDPOINT, minio_url, access_key, secret_key)
        # End timing
        end_time = time.time()
        # Calculate and print the duration
        duration = end_time - start_time
        print(f"Finished in {duration} seconds")


    def run_local_files():
        start_time = time.time()
        path = f"/home/dzailz/Downloads/golos_opus/train_opus/crowd/{random.choice(range(0, 10))}"
        send_random_file_from_disk(path=path, endpoint=ENDPOINT)
        time.sleep(random.randint(1, 33))
        end_time = time.time()
        # Calculate and print the duration
        duration = end_time - start_time
        print(f"Finished in {duration} seconds")


    overall_start_time = time.time()
    for i in range(50):
        print(f"{i} file")
        run_local_files()
    overall_end_time = time.time()
    print(f"Finished in {overall_end_time - overall_start_time} seconds")
