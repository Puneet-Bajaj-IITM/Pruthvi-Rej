Here's a comprehensive `README.md` for your codebase that explains its functionality and usage. This should help other developers understand the structure of your project and how to extend it.

---

# Movie Script and Audio Processing App

## Overview

This project is a Streamlit-based application designed to handle and process movie scripts and corresponding audio files. It integrates with Google Cloud Storage and OpenAI APIs for classification, translation, and similarity analysis. The application performs the following main tasks:

1. **Upload and Classify Movie Scripts**: Upload movie scripts and classify them as valid or invalid.
2. **Upload and Analyze Audio Files**: Upload corresponding audio files, translate them, and compute similarity with the scripts.
3. **Upload Processed Data to Google Cloud Storage**: Store scripts, audio files, and embeddings in Google Cloud Storage.

## Project Structure

### `app.py`

The main entry point for the Streamlit application. It handles user interactions and integrates various functionalities.

#### Key Functions

- **`check_password()`**: Prompts the user for a password to secure access to the application.
- **Session Initialization**: Sets up session state variables to store various states and paths.
- **File Upload**:
  - **Script Upload**: Allows users to upload movie scripts and validates them.
  - **Audio Upload**: Allows users to upload corresponding audio files once the script is validated.
- **File Handling**:
  - **Script Processing**: Uses `handle_file_upload_with_confidence()` to process and validate scripts.
  - **Audio Processing**: Uses `handle_audio_upload_with_confidence()` to translate and analyze audio files.

### `config.py`

Configuration file that sets environment variables and defines paths and parameters used across the application.

#### Key Settings

- **Google Cloud and OpenAI Keys**: Environment variables for API keys.
- **Directory Paths**: Paths for text and audio files, and human evaluation.
- **Supported Formats**: Lists of supported script and audio formats.
- **Thresholds**: Confidence and similarity thresholds used for processing.

### `file_handlers.py`

Contains functions to handle file uploads and processing with confidence.

#### Key Functions

- **`handle_file_upload_with_confidence()`**: Loads documents from the text directory, classifies them, and returns the classification results.
- **`handle_audio_upload_with_confidence()`**: Processes audio files, translates them, computes embeddings, and uploads data to Google Cloud Storage.

### `utils/`

A folder containing utility modules for various tasks.

#### `audio_utils.py`

Handles audio file translations.

- **`get_translation_with_confidence()`**: Translates audio files using the OpenAI API and filters them based on confidence.

#### `cloud_utils.py`

Manages interactions with Google Cloud Storage.

- **`upload_directory_to_gcloud_with_confidence()`**: Uploads validated script files to Google Cloud Storage.
- **`upload_embeddings_to_gcs()`**: Uploads text embeddings to Google Cloud Storage.
- **`upload_audio_to_gcloud()`**: Uploads validated audio files to Google Cloud Storage.

#### `doc_utils.py`

Handles document loading and processing.

- **`load_file()`**: Loads files from a given folder based on their format (PDF, TXT, DOCX).

### `requiremnt.txt`

Lists the required Python packages for the project.

## Setup Instructions

1. **Install Dependencies**:

   Ensure you have the necessary Python packages installed:

   ```bash
   pip install -r requiremnt.txt
   ```

2. **Set Up Environment Variables**:

   Update `config.py` with your Google Cloud and OpenAI API keys. Ensure the `GOOGLE_APPLICATION_CREDENTIALS` points to your Google Cloud credentials JSON file.

3. **Create Required Directories**:

   Make sure the directories specified in `config.py` exist or will be created automatically.

4. **Run the Application**:

   Start the Streamlit application by running:

   ```bash
   streamlit run app.py
   ```

## Extending the Application

To extend the functionality of this application, consider the following:

1. **Add New File Types**:
   - Update `config.py` to include new supported script and audio formats.
   - Modify `file_handlers.py` and `audio_utils.py` to handle these new formats.

2. **Improve Classification and Translation**:
   - Enhance the classification logic in `file_handlers.py`.
   - Update `audio_utils.py` to use more advanced translation models or APIs.

3. **Expand Cloud Storage Capabilities**:
   - Modify `cloud_utils.py` to include additional storage options or features.

4. **Add New Features**:
   - Implement additional functionalities in `app.py` for new user interactions or processing steps.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to adjust the README to better fit any additional details or specific instructions relevant to your project.