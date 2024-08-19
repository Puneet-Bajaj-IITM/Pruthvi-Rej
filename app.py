import hmac
import streamlit as st
import os
import time
import shutil
from config import text_dir, audio_dir, supported_audio_formats, supported_script_formats, human_eval_path
from google.cloud import storage
from openai import OpenAI
from file_handlers import handle_file_upload_with_confidence, handle_audio_upload_with_confidence
from sentence_transformers import SentenceTransformer, util

# Initialize storage and OpenAI clients
storage_client = storage.Client()
client = OpenAI()


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Initialize session state variables
if 'classification' not in st.session_state:
    st.session_state.classification = {}

if 'model' not in st.session_state:
    st.session_state.model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

if 'util' not in st.session_state:
    st.session_state.util = util

if 'movie_name' not in st.session_state:
    st.session_state.movie_name = ''

if 'lang' not in st.session_state:
    st.session_state.lang = ''

if 'script_path' not in st.session_state:
    st.session_state.script_path = ''

if 'audio_file_path' not in st.session_state:
    st.session_state.audio_file_path = ''

if 'human_eval' not in st.session_state:
    st.session_state.human_eval = human_eval_path

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = ''

if 'file_data' not in st.session_state:
    st.session_state.file_data = {}

if 'translated_text' not in st.session_state:
    st.session_state.translated_text = {}

if 'first_upload_complete' not in st.session_state:
    st.session_state.first_upload_complete = False

if 'second_upload_complete' not in st.session_state:
    st.session_state.second_upload_complete = False

# Ensure the text directory is ready for use
upload_directory = text_dir
if os.path.exists(upload_directory):
    shutil.rmtree(upload_directory)
os.makedirs(upload_directory)

if not os.path.exists(human_eval_path):
    os.makedirs(human_eval_path)

audio_upload_directory = audio_dir
if os.path.exists(audio_upload_directory):
    shutil.rmtree(audio_upload_directory)
os.makedirs(audio_upload_directory)

st.session_state.audio_upload_directory = audio_upload_directory
st.session_state.upload_directory = upload_directory

# File uploader widget for general files
st.session_state.movie_name = st.text_input(
    label='Movie Name', placeholder='Enter Movie Name here.......')
if st.session_state.movie_name:
    st.session_state.lang = st.text_input(
        label='Movie Lnaguage', placeholder='Enter Movie Language here.........')
if st.session_state.movie_name and st.session_state.lang:
    st.write('Drag a Script to below box 👇')
    st.session_state.uploaded_file = st.file_uploader(
        "Upload a Script", type=supported_script_formats, accept_multiple_files=False)

if st.session_state.uploaded_file:
    file_name = f"{st.session_state.movie_name}-{st.session_state.lang}-001.{st.session_state.uploaded_file.name.split('.')[-1]}"
    file_path = os.path.join(st.session_state.upload_directory, file_name)
    st.session_state.script_path = file_path
    with open(file_path, "wb") as f:
        f.write(st.session_state.uploaded_file.getvalue())
    st.write(f"Processing File: {st.session_state.uploaded_file.name}")
    st.session_state.uploaded_file = file_name.split('.')[0]

    # Handle the uploaded files
    st.session_state.classification, st.session_state.file_data = handle_file_upload_with_confidence()
    st.session_state.first_upload_complete = not all(value.get(
        'script') == '<|NO|>' for value in st.session_state.classification.values())
    if not st.session_state.first_upload_complete:
        st.write('Not a Script ❌')
        st.write('Please Refresh Page to Upload New Scripts')
    else:
        st.write('Identified as a Script ✅')


# Show the audio file upload box only after the first step is complete
if st.session_state.first_upload_complete:
    st.write('Drag Narration to below box 👇')
    uploaded_audio_file = st.file_uploader(
        "Upload Corresponding Narration", type=supported_audio_formats, accept_multiple_files=False)

    if uploaded_audio_file:

        audio_file_path = os.path.join(st.session_state.audio_upload_directory,
                                           st.session_state.uploaded_file + '.' + uploaded_audio_file.name.split('.')[-1])
        st.session_state.audio_file_path = audio_file_path

        with open(audio_file_path, "wb") as f:
            f.write(uploaded_audio_file.getvalue())
        st.write(f"Processing Audio file: {uploaded_audio_file.name}")
        global model
        similarity_below_thresh = handle_audio_upload_with_confidence(storage_client, client, st.session_state.classification, st.session_state.model, st.session_state.util)
        if similarity_below_thresh:
            st.write('Similarity below threshold ❌')
            if st.button('Click to Apply For Human Evaluation'):
                shutil.move(st.session_state.audio_file_path, st.session_state.human_eval)
                shutil.move(st.session_state.script_path, st.session_state.human_eval)
                st.write('We will verify manually!!')
        else:
            st.write('Saved successfully !! ✅')
            
        st.session_state.second_upload_complete = True
        st.write('Please Refresh Page to Upload New Scripts')