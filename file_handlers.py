from utils.audio_utils import get_translation_with_confidence
from utils.cloud_utils import upload_audio_to_gcloud, upload_directory_to_gcloud_with_confidence, upload_embeddings_to_gcs
from utils.doc_utils import load_directory
from config import *
from utils.embedding_utils import embed_text_with_confidence
from utils.script_utils import classifier, validate_scripts_with_confidence
from utils.similarity_utils import compute_similarity

def handle_file_upload_with_confidence():
    # Load the docs from directory
    file_data = load_directory(text_dir)

    # Set the LLM
    llm = classifier(temperature, model)

    # Validate Scripts to Script or not (<|YES|> or <|NO|>)
    classification = validate_scripts_with_confidence(llm, file_data)

    return classification, file_data
    
def handle_audio_upload_with_confidence(storage_client, client, classification, model, util):
    
    # Load the audio file
    translated_text = get_translation_with_confidence(classification, confidence_threshold, client, audio_dir, supported_audio_formats)

    # Embed the text
    embedded_text = embed_text_with_confidence(classification, confidence_threshold, translated_text, model)
    

    similarity = compute_similarity(embedded_text, util)

    if not all(value >= threshold for value in similarity.values()):
        return True

    # Upload all Scripts to Cloud
    upload_directory_to_gcloud_with_confidence(classification, confidence_threshold, storage_client, text_dir, bucket_name, doc_bkt, supported_script_formats)

    # Save the embeddings to Embedding folder
    upload_embeddings_to_gcs(storage_client, similarity, embedded_text, bucket_name, folder_name, threshold)

    # Upload all audio to Cloud
    upload_audio_to_gcloud(similarity, storage_client, audio_dir, bucket_name, audio_bkt, supported_audio_formats, threshold)
    
    return False