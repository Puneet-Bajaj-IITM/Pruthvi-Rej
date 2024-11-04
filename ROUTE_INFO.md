## Endpoints

### 1. `/upload/script` (POST)
Uploads a movie script file. Validates if the uploaded file is recognized as a script. If valid, the script is saved on the server.

#### Request Parameters
- **`movie_name`** (form data): Name of the movie (string).
- **`lang`** (form data): Language of the script (string).
- **`script_file`** (file): Script file to be uploaded (file, required).

#### Response
- **Success (200)**: 
  ```json
  {
    "message": "Script uploaded successfully."
  }
  ```
- **Failure (400)**:
  ```json
  {
    "error": "Not a Script ❌"
  }
  ```

#### Example `curl` Request

```bash
curl -X POST http://localhost:5000/upload/script \
  -F "movie_name=Inception" \
  -F "lang=en" \
  -F "script_file=@/path/to/script.txt"
```

### 2. `/upload/narration` (POST)
Uploads an audio narration file. Compares the uploaded audio file with stored information to verify similarity and thresholds.

#### Request Parameters
- **`movie_name`** (form data): Name of the movie (string).
- **`lang`** (form data): Language of the audio file (string).
- **`audio_file`** (file): Audio file for narration (file, required).

#### Response
- **Success (200)**: 
  ```json
  {
    "message": "Audio file is the narration of uploaded script !! ✅"
  }
  ```
- **Failure (400)**:
  - If the file is not an audio file:
    ```json
    {
      "error": "No audio File uploaded"
    }
    ```
  - If similarity is below the threshold:
    ```json
    {
      "error": "Similarity below threshold ❌"
    }
    ```

#### Example `curl` Request

```bash
curl -X POST http://localhost:5000/upload/narration \
  -F "movie_name=Inception" \
  -F "lang=en" \
  -F "audio_file=@/path/to/narration.mp3"
```

---

## Setup

1. **Environment Variables**:
   - `FLASK_SECRET_KEY`: Recommended for securely storing the Flask secret key.

2. **Dependencies**:
   - Python 3.12, Flask, `google-cloud-storage`, `openai`, `sentence-transformers`

3. **Running the Server**:
   ```bash
   pip install -r requirements.txt
   python flask_app.py
   ```
