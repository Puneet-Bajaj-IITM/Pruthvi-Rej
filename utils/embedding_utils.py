from langchain_openai import OpenAIEmbeddings

def embed_text_with_confidence(classification, confidence_threshold, translated_text):
    embeddings = OpenAIEmbeddings()
    d = {}
    for file in translated_text:
       if file not in classification:
            continue
       if classification[file]['script'].strip() == '<|NO|>':
            continue
       if classification[file]['confidence'] < confidence_threshold:
            continue
       d[file] = {
          "doc_content": embeddings.embed_query(translated_text[file]['doc_content']),
          "audio_translation": embeddings.embed_query(translated_text[file]['audio_translation'])
        }
    return d