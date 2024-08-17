
def embed_text_with_confidence(classification, confidence_threshold, translated_text, model):
    d = {}
    for file in translated_text:
       if file not in classification:
            continue
       if classification[file]['script'].strip() == '<|NO|>':
            continue
       if classification[file]['confidence'] < confidence_threshold:
            continue
       d[file] = {
          "doc_content": model.encode(translated_text[file]['doc_content'], convert_to_tensor=True),
          "audio_translation":  model.encode(translated_text[file]['audio_translation'], convert_to_tensor=True)
        }
    return d