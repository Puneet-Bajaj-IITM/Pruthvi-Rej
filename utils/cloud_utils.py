from google.cloud import storage
import streamlit as st
import json
import os

def upload_directory_to_gcloud_with_confidence(classification, confidence_threshold, storage_client, directory_path, bucket_name, folder_name, supported_formats):
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        name = filename.split('.')[0]

        if name not in classification:
            continue
        if classification[name]['script'].strip() == '<|NO|>':
            st.warning(f'{filename} doesn\'t look like a script', icon="⚠️")
            continue
        if classification[name]['confidence'] < confidence_threshold:
            st.warning(f'{filename} below Threshold', icon="⚠️")
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

            st.success(f'Identified {filename} as Script', icon="✅")

def upload_embeddings_to_gcs(storage_client, similarity, embedded_text, bucket_name, folder_name, threshold=0.7):
    bucket = storage_client.get_bucket(bucket_name)
    # Iterate over the dictionary and save each embedding as a JSON file in GCS
    for key, value in embedded_text.items():
        if key not in similarity:
            st.warning(f'No Corresponding File to {key}', icon="⚠️")
            continue
        if similarity[key] < threshold:
            st.warning(f'Similarity below Threshold for {key}', icon="⚠️")
            continue
        # Convert the embedding to a JSON string
        embedding_json = json.dumps(value)

        # Define the file path in the GCS bucket
        file_name = f'{folder_name}/{key}.json'

        # Create a blob object for the file
        blob = bucket.blob(file_name)

        # Upload the JSON string to GCS
        blob.upload_from_string(embedding_json, content_type='application/json')

        print(f'Successfully uploaded {key}.json to {bucket_name}/{file_name}')
        
def upload_audio_to_gcloud(similarity, storage_client, audio_dir, bucket_name, audio_bkt, supported_formats, threshold):
    # Iterate over all files in the specified directory
    for filename in os.listdir(audio_dir):
        file_path = os.path.join(audio_dir, filename)

        name = filename.split('.')[0]

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

            st.success(f'Identified {filename} as Narration', icon="✅")
