
def compute_similarity(embedded_text, util):
    d = {}

    for file in embedded_text:

        # Generate embeddings
        doc_content_embedding = embedded_text[file]['doc_content']
        audio_translation_embedding = embedded_text[file]['audio_translation']

        # Compute similarity
        similarity = util.pytorch_cos_sim(doc_content_embedding, audio_translation_embedding)
        print(similarity)

        # Store embeddings and similarity in dictionary
        d[file] =  float("{:.4f}".format(similarity[0][0]))

    return d
