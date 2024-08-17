import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'long-star-431222-t8-9e46375fea09.json'
os.environ['OPENAI_API_KEY'] = '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'
os.environ["GOOGLE_API_KEY"] =  'AIzaSyDxiTc2ddsA5AzOAwWCs3Gez7p2s0dc4Ls'

# Define the text directory
text_dir = 'uploads/files'

model = 'gemini-1.5-flash-latest'
temperature = 0

bucket_name = 'movie-script'
doc_bkt = 'documents'
confidence_threshold = 0.8
supported_script_formats = ['pdf', 'txt', 'docx']

bucket_name = 'movie-script'
folder_name = 'embeddings'
threshold = 0.7

# Define audio file path
audio_dir = 'uploads/audio'
supported_audio_formats = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']

audio_bkt = 'audio'





finetuning_criteria = """
Q) How do you determine if it is a script or not?

Scene Headings (Sluglines): These are used to indicate the location and time of day of a scene. They typically follow the format: "INT." or "EXT." (indoor/outdoor), the location, and the time of day (e.g., "INT. COFFEE SHOP - DAY"). Example: INT. COMPUTER ROOM - DAY (Scene Heading)
Action Descriptions: These provide a visual description of the action happening on the screen. They are written in the present tense.
Example of scene and action:

5. INT. COMPUTER ROOM - DAY

We see the camera is placed on the table. With the memory card on the hand placing it on the card holder.

We see downloading file in the computer. And we see the files are exporting it to the different WhatsApp groups... here we have to register a different group name.

Character Names: When a character speaks, their name is typically centered and in uppercase.
Dialogue: This follows the character name and is usually indented.
Examples of character and dialogues

SUBBU MOTHER
Good morning....night nedra patindha...?

RITU
Ha aunty bane patindhi

SUBBU FATHER
Good morning amma

RITU
Good morning uncle

SUBBU FATHER
Vadu inka levaledha..?

Transition Directions: Words like "CUT TO:" or "FADE IN:" are used to indicate transitions between scenes.
Note: Create features based on the frequency of scene headings, character names, dialogue, transitions, etc. Analyze sentence structure to distinguish between action descriptions and dialogue.
"""



