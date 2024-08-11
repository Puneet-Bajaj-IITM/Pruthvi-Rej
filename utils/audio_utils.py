import os

def get_translation_with_confidence(classification, confidence_threshold, client, file_data, audio_dir, supported_formats):
    d = {}
    for audio_file in os.listdir(audio_dir):
        name = audio_file.split('.')[0]

        if name not in classification:
            continue
        if classification[name]['script'].strip() == '<|NO|>':
            continue
        if classification[name]['confidence'] < confidence_threshold:
            continue
        ext = audio_file.split('.')[1]
        if ext not in supported_formats:
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