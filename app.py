import streamlit as st
import os
import shutil
from config import text_dir, audio_dir, supported_audio_formats, supported_script_formats
from google.cloud import storage
from openai import OpenAI
from file_handlers import handle_file_upload_with_confidence, handle_audio_upload_with_confidence

# Initialize storage and OpenAI clients
storage_client = storage.Client()
client = OpenAI()

import hmac
import streamlit as st


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

if 'file_data' not in st.session_state:
    st.session_state.file_data = {}

if 'translated_text' not in st.session_state:
    st.session_state.translated_text = {}

if 'first_upload_complete' not in st.session_state:
    st.session_state.first_upload_complete = False

# Ensure the text directory is ready for use
upload_directory = text_dir
if os.path.exists(upload_directory):
    shutil.rmtree(upload_directory)
os.makedirs(upload_directory)

audio_upload_directory = audio_dir
if os.path.exists(audio_upload_directory):
    shutil.rmtree(audio_upload_directory)
os.makedirs(audio_upload_directory)

st.session_state.audio_upload_directory = audio_upload_directory
st.session_state.upload_directory = upload_directory

# File uploader widget for general files
uploaded_files = st.file_uploader("Choose files",type=supported_script_formats, accept_multiple_files=True)

if uploaded_files and st.button("Upload Files"):
    for uploaded_file in uploaded_files:
        file_path = os.path.join(st.session_state.upload_directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.write(f"File saved at: {file_path}")

    # Handle the uploaded files
    st.session_state.classification, st.session_state.file_data = handle_file_upload_with_confidence(storage_client)
    st.session_state.first_upload_complete = True

# Show the audio file upload box only after the first step is complete
if st.session_state.first_upload_complete:
    uploaded_audio_files = st.file_uploader("Upload audio files", type=supported_audio_formats, accept_multiple_files=True)

    if uploaded_audio_files and st.button("Upload Audio Files"):
        for uploaded_audio_file in uploaded_audio_files:
            audio_file_path = os.path.join(st.session_state.audio_upload_directory, uploaded_audio_file.name)
            with open(audio_file_path, "wb") as f:
                f.write(uploaded_audio_file.getvalue())
            st.write(f"Audio file saved at: {audio_file_path}")

        handle_audio_upload_with_confidence(storage_client, client, st.session_state.classification, st.session_state.file_data)
