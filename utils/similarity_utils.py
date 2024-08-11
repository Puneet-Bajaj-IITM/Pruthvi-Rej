from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def cos_similarity(doc_embedding, audio_embedding):
    # Ensure embeddings are 2D for scikit-learn cosine_similarity
    doc_embedding = np.array(doc_embedding).reshape(1, -1)
    audio_embedding = np.array(audio_embedding).reshape(1, -1)

    # Compute cosine similarity
    similarity = cosine_similarity(doc_embedding, audio_embedding)

    return similarity[0][0]

def compute_similarity(embedded_text):
    d = {}

    for file in embedded_text:

        # Generate embeddings
        doc_content_embedding = embedded_text[file]['doc_content']
        audio_translation_embedding = embedded_text[file]['audio_translation']

        # Compute similarity
        similarity = cos_similarity(doc_content_embedding, audio_translation_embedding)

        # Store embeddings and similarity in dictionary
        d[file] =  similarity

    return d
