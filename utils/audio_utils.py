import os
import streamlit as st

def get_translation_with_confidence(classification, confidence_threshold, client, audio_dir, supported_formats):
    """
    Translates audio files based on their classification and confidence.

    Parameters:
    - classification (dict): Dictionary containing the classification results.
    - confidence_threshold (float): The minimum confidence score required for processing an audio file.
    - client (object): The client object used to interact with the translation service.
    - audio_dir (str): Directory containing the audio files to be processed.
    - supported_formats (set): Set of supported audio file formats.

    Returns:
    - dict: A dictionary where keys are file names and values are dictionaries containing 
            the document content and audio translation.
    """
    d = {}  # Initialize an empty dictionary to store translations
    
    # Iterate through all files in the specified audio directory
    for audio_file in os.listdir(audio_dir):
        # Extract the base name (without extension) and file extension
        name = audio_file.split('.')[0]
        ext = audio_file.split('.')[1]

        # Check if the file's name is in the classification dictionary
        if name not in classification:
            st.write(f"Document not Found", icon="❌")
            continue

        # Skip files where the script is marked as '<|NO|>'
        if classification[name]['script'].strip() == '<|NO|>':
            st.write(f"Skipping audio as its not Found to be a script", icon="❌")
            continue

        # Skip files with confidence below the specified threshold
        if classification[name]['confidence'] < confidence_threshold:
            st.write(f"Skipping audio as confidence below threshold ({confidence_threshold})", icon="❌")
            continue

        # Skip files with unsupported formats
        if ext not in supported_formats:
            st.write(f"Skipping audio, not in expected format", icon="❌")
            continue
        
        file_name = os.path.basename(audio_file).split('.')[0]
        audio_file_path = os.path.join(audio_dir, audio_file)
        
        # Define the maximum file size (24 MB)
        MAX_FILE_SIZE = 24 * 1024 * 1024
        
        # Get the size of the current audio file
        audio_file_size = os.path.getsize(audio_file_path)
        
        # Handle files larger than the maximum allowed size
        if audio_file_size > MAX_FILE_SIZE:
            with open(audio_file_path, "rb") as audio_file:
                partial_audio_data = audio_file.read(MAX_FILE_SIZE)
                
            partial_file_path = f'uploads/{file_name}.{ext}'
            with open(partial_file_path, "wb") as partial_audio_file:
                partial_audio_file.write(partial_audio_data)

            # Read back the saved partial file
            audio_data = open(partial_file_path, "rb")
            os.remove(partial_file_path)
        else:
            audio_data = open(audio_file_path, "rb")
        
        # Request translation from the client
        translation = client.audio.translations.create(
          model="whisper-1",
          file=audio_data
        )
        
        # Initialize dictionary entry if not present
        if file_name not in d:
            d[file_name] = {
                "doc_content": classification[file_name]['summary'],
                "audio_translation": ''
            }
        d[file_name]["audio_translation"] = translation.text
    
    return d
