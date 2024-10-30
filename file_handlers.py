from utils.audio_utils import get_translation_with_confidence
from utils.cloud_utils import upload_audio_to_gcloud, upload_directory_to_gcloud_with_confidence, upload_embeddings_to_gcs
from utils.doc_utils import load_directory
from config import *
from utils.embedding_utils import embed_text_with_confidence
from utils.script_utils import classifier, validate_scripts_with_confidence
from utils.similarity_utils import compute_similarity

def handle_file_upload_with_confidence():
    """
    Handles the process of loading documents from a directory, setting up the language model,
    and validating the scripts for further processing.

    Returns:
        tuple: A tuple containing:
            - classification (dict): The result of script classification with confidence scores.
            - file_data (dict): The loaded file data from the specified directory.
    """
    # Load the documents from the specified directory
    file_data = load_directory(text_dir)

    # Initialize the language model (LLM) with specified parameters
    llm = classifier(temperature, model)

    # Validate the scripts and get the classification results with confidence scores
    classification = validate_scripts_with_confidence(llm, file_data)

    return classification, file_data

def handle_audio_upload_with_confidence(storage_client, client, classification, model, util):
    """
    Processes audio files by translating them, embedding the translated text, 
    computing similarity scores, and uploading results to cloud storage.

    Args:
        storage_client (object): The client used for interacting with cloud storage.
        client (object): The client used for interacting with audio services.
        classification (dict): The result of script classification with confidence scores.
        model (object): The model used for embedding text.
        util (object): Utility object used for similarity computation.

    Returns:
        bool: Returns True if any similarity value is below the threshold, otherwise False.
    """
    # Translate the audio file and obtain the translated text with confidence scores
    translated_text = get_translation_with_confidence(
        classification, confidence_threshold, client, audio_dir, supported_audio_formats
    )

    # Embed the translated text with confidence scores
    embedded_text = embed_text_with_confidence(
        classification, confidence_threshold, translated_text, model
    )

    # Compute similarity scores between the embedded text and utility object
    similarity = compute_similarity(embedded_text, util)

    # Check if all similarity values meet or exceed the threshold
    if not all(value >= threshold for value in similarity.values()):
        return True

    # # Upload the validated scripts to Google Cloud Storage
    # upload_directory_to_gcloud_with_confidence(
    #     classification, confidence_threshold, storage_client, text_dir, bucket_name, doc_bkt, supported_script_formats
    # )

    # # Save the embeddings to Google Cloud Storage
    # upload_embeddings_to_gcs(
    #     storage_client, similarity, embedded_text, bucket_name, folder_name, threshold
    # )

    # # Upload the audio files to Google Cloud Storage
    # upload_audio_to_gcloud(
    #     similarity, storage_client, audio_dir, bucket_name, audio_bkt, supported_audio_formats, threshold
    # )
    
    return False
