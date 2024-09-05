from google.cloud import storage
import streamlit as st
import json
import os

def upload_directory_to_gcloud_with_confidence(classification, confidence_threshold, storage_client, directory_path, bucket_name, folder_name, supported_formats):
    """
    Uploads files from a local directory to Google Cloud Storage (GCS) if they meet certain criteria.
    
    Args:
        classification (dict): A dictionary where keys are filenames (without extension) and values are dicts 
                                containing 'script' and 'confidence' fields.
        confidence_threshold (float): Minimum confidence required for a file to be uploaded.
        storage_client (google.cloud.storage.Client): Google Cloud Storage client.
        directory_path (str): Local path to the directory containing files to be uploaded.
        bucket_name (str): Name of the GCS bucket where files will be uploaded.
        folder_name (str): Folder name within the bucket where files will be stored.
        supported_formats (list): List of file extensions that are supported for upload.
    """
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        name = filename.split('.')[0]

        # Check if the file is classified and meets the confidence threshold
        if name not in classification:
            continue
        if classification[name]['script'].strip() == '<|NO|>':
            st.write(f'{filename} doesn\'t look like a script', icon="⚠️")
            continue
        if classification[name]['confidence'] < confidence_threshold:
            st.write(f'{filename} below Threshold', icon="⚠️")
            continue

        # Check if the file has a supported format
        ext = filename.split('.')[1]
        if ext not in supported_formats:
            continue

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Construct the destination path in the bucket
            destination_blob_name = f'{folder_name}/{filename}'

            # Upload the file to the specified bucket and path
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_path)

            st.write(f'Identified {filename} as Script', icon="✅")
        os.remove(file_path)

def convert_to_json_serializable(dic):
    """
    Converts a dictionary with numpy arrays to a JSON-serializable dictionary.

    Args:
        dic (dict): Dictionary where values are numpy arrays.
    
    Returns:
        dict: JSON-serializable dictionary with arrays converted to lists.
    """
    json_serial = {}
    for key, val in dic.items():
        json_serial[key] = val.tolist()
    return json_serial

def upload_embeddings_to_gcs(storage_client, similarity, embedded_text, bucket_name, folder_name, threshold=0.7):
    """
    Uploads embedding files to Google Cloud Storage (GCS) if they meet a similarity threshold.

    Args:
        storage_client (google.cloud.storage.Client): Google Cloud Storage client.
        similarity (dict): Dictionary where keys are identifiers and values are similarity scores.
        embedded_text (dict): Dictionary where keys are identifiers and values are embedding data.
        bucket_name (str): Name of the GCS bucket where files will be uploaded.
        folder_name (str): Folder name within the bucket where files will be stored.
        threshold (float, optional): Minimum similarity score required for a file to be uploaded. Defaults to 0.7.
    """
    bucket = storage_client.get_bucket(bucket_name)
    
    # Iterate over the dictionary and save each embedding as a JSON file in GCS
    for key, value in embedded_text.items():
        if key not in similarity:
            st.write(f'No Corresponding File to {key}', icon="⚠️")
            continue
        if similarity[key] < threshold:
            st.write(f'Similarity ({similarity[key]}) below Threshold ({threshold}) for {key}', icon="⚠️")
            continue

        # Convert the embedding to a JSON string
        json_value = convert_to_json_serializable(value)
        embedding_json = json.dumps(json_value)

        # Define the file path in the GCS bucket
        file_name = f'{folder_name}/{key}.json'

        # Create a blob object for the file
        blob = bucket.blob(file_name)

        # Upload the JSON string to GCS
        blob.upload_from_string(embedding_json, content_type='application/json')

        print(f'Successfully uploaded {key}.json to {bucket_name}/{file_name}')
        
def upload_audio_to_gcloud(similarity, storage_client, audio_dir, bucket_name, audio_bkt, supported_formats, threshold):
    """
    Uploads audio files from a local directory to Google Cloud Storage (GCS) if they meet a similarity threshold.

    Args:
        similarity (dict): Dictionary where keys are filenames (without extension) and values are similarity scores.
        storage_client (google.cloud.storage.Client): Google Cloud Storage client.
        audio_dir (str): Local path to the directory containing audio files to be uploaded.
        bucket_name (str): Name of the GCS bucket where files will be uploaded.
        audio_bkt (str): Folder name within the bucket where audio files will be stored.
        supported_formats (list): List of file extensions that are supported for upload.
        threshold (float): Minimum similarity score required for a file to be uploaded.
    """
    # Iterate over all files in the specified directory
    for filename in os.listdir(audio_dir):
        file_path = os.path.join(audio_dir, filename)
        name = filename.split('.')[0]

        # Check if the file is classified and meets the similarity threshold
        if name not in similarity:
            continue
        if similarity[name] < threshold:
            continue

        # Check if the file has a supported format
        ext = filename.split('.')[1]
        if ext not in supported_formats:
            continue

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Construct the destination path in the bucket
            destination_blob_name = f'{audio_bkt}/{filename}'

            # Upload the file to the specified bucket and path
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_path)

            st.write(f'Identified {filename} as Narration', icon="✅")
        os.remove(file_path)
