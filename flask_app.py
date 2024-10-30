import hmac
import os
import shutil
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from config import text_dir, audio_dir, supported_audio_formats, supported_script_formats, human_eval_path
from google.cloud import storage
from openai import OpenAI
from file_handlers import handle_file_upload_with_confidence, handle_audio_upload_with_confidence
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
app.secret_key = 'my_secure_key'  # Set a secure secret key for session management

# Initialize Google Cloud Storage and OpenAI clients
storage_client = storage.Client()
client = OpenAI()

# Initialize sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

@app.route('/upload', methods=['POST'])
def upload():
    password = request.form.get('password')
    if password == os.environ['PASSWORD']:  # Store the password in environment variables
        session['logged_in'] = True    
    else:          
        return "Password incorrect", 403

    if session.get('logged_in'):
        movie_name = request.form.get('movie_name')
        lang = request.form.get('lang')
        script_file = request.files.get('script_file')
        audio_file = request.files.get('audio_file')

        if script_file:
            file_name = f"{movie_name}-{lang}-001.{script_file.filename.split('.')[-1]}"
            script_path = os.path.join(text_dir, file_name)
            script_file.save(script_path)
            classification, file_data = handle_file_upload_with_confidence()
            first_upload_complete = not all(value.get('script') == '<|NO|>' for value in classification.values())

            if not first_upload_complete:
                return jsonify({"error": "Not a Script ❌"}), 400
            
            # If script upload is complete, handle audio upload
            if audio_file:
                audio_path = os.path.join(audio_dir, f"{file_name.split('.')[0]}.{audio_file.filename.split('.')[-1]}")
                audio_file.save(audio_path)

                similarity_below_thresh = handle_audio_upload_with_confidence(storage_client, client, classification, model, util)
                if similarity_below_thresh:
                    return jsonify({"error": "Similarity below threshold ❌"}), 400
                
                return jsonify({"message": "Files saved successfully !! ✅"}), 200
            
            return jsonify({"message": "Script uploaded successfully."}), 200


if __name__ == '__main__':
    # Ensure necessary directories exist
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(human_eval_path, exist_ok=True)

    app.run(debug=True)
