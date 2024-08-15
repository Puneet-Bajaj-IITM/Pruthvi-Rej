import os
import streamlit as st

def get_translation_with_confidence(classification, confidence_threshold, client, file_data, audio_dir, supported_formats):
    d = {}
    for audio_file in os.listdir(audio_dir):
        name = audio_file.split('.')[0]

        if name not in classification:
            st.success(f"Document with Name '{name}' not Found", icon="❌")
            continue
        if classification[name]['script'].strip() == '<|NO|>':
            st.success(f"Skipping audio '{name}' as its not Found to be a script", icon="❌")
            continue
        if classification[name]['confidence'] < confidence_threshold:
            st.success(f"Skipping audio '{name}' as confidence below threshold ({confidence_threshold})", icon="❌")
            continue
        ext = audio_file.split('.')[1]
        if ext not in supported_formats:
            st.success(f"Skipping audio '{name}' , not in expected format", icon="❌")
            continue
        file_name = os.path.basename(audio_file).split('.')[0]
        audio_file_path = os.path.join(audio_dir, audio_file)
        audio_file = open(audio_file_path, "rb")
        translation = client.audio.translations.create(
          model="whisper-1",
          file=audio_file
        )
        if file_name not in d:
            d[file_name] = {
                "doc_content": file_data[file_name],
                "audio_translation": ''
            }
        d[file_name]["audio_translation"] = translation.text
    return d