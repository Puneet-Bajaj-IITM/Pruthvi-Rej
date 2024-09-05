def embed_text_with_confidence(classification, confidence_threshold, translated_text, model):
    """
    Embeds text from the translated_text dictionary based on classification confidence and script criteria.

    Args:
        classification (dict): A dictionary containing classification details for each file. 
            Keys should be filenames, and values should be dictionaries with keys 'script' and 'confidence'.
        confidence_threshold (float): The minimum confidence score required to include a file.
        translated_text (dict): A dictionary containing translated text for each file. 
            Keys should be filenames, and values should be dictionaries with 'doc_content' and 'audio_translation'.
        model (object): A model with an `encode` method used to convert text into tensor embeddings.

    Returns:
        dict: A dictionary with filenames as keys and embedding data as values. Each value is a dictionary with keys
              'doc_content' and 'audio_translation', containing tensor embeddings of the respective content.
    """
    d = {}
    for file in translated_text:
        # Skip files that are not present in the classification dictionary
        if file not in classification:
            continue
        
        # Skip files with '<|NO|>' as the script value
        if classification[file]['script'].strip() == '<|NO|>':
            continue
        
        # Skip files with confidence scores below the threshold
        if classification[file]['confidence'] < confidence_threshold:
            continue
        
        # Add embeddings for files that meet the criteria
        d[file] = {
            "doc_content": model.encode(translated_text[file]['doc_content'], convert_to_tensor=True),
            "audio_translation": model.encode(translated_text[file]['audio_translation'], convert_to_tensor=True)
        }
    return d
