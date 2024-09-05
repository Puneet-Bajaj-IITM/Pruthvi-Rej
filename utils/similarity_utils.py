def compute_similarity(embedded_text, util):
    """
    Compute the similarity between document content and audio translation embeddings.

    Args:
        embedded_text (dict): A dictionary where keys are file names and values are dictionaries containing
                              'doc_content' and 'audio_translation' tensors. Each tensor represents
                              the embeddings for document content and audio translation, respectively.
        util (object): An object with a method `pytorch_cos_sim` for computing cosine similarity between tensors.

    Returns:
        dict: A dictionary where keys are file names and values are the computed similarity scores (float).
    """
    d = {}  # Initialize an empty dictionary to store similarity results

    for file in embedded_text:
        # Extract embeddings for document content and audio translation
        doc_content_embedding = embedded_text[file]['doc_content']
        audio_translation_embedding = embedded_text[file]['audio_translation']

        # Compute cosine similarity between the document content and audio translation embeddings
        similarity = util.pytorch_cos_sim(doc_content_embedding, audio_translation_embedding)
        print(similarity)  # Print the similarity score for debugging purposes

        # Format the similarity score to 4 decimal places and store it in the dictionary
        d[file] = float("{:.4f}".format(similarity[0][0]))

    return d  # Return the dictionary containing the similarity scores
