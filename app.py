# -*- coding: utf-8 -*-
"""Pruthvi-Runway.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1c_5MDn636QMEhyDhS4uBWGpV3Ko-krC8
"""

# Commented out IPython magic to ensure Python compatibility.
# install package


from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

def create_stage_prompt(stage, inputs):
    """
    Create a structured video generation prompt for a specific stage in a narrative, based on user inputs.

    Parameters:
    - stage (str): The name of the stage (e.g., "Introduction", "Climax").
    - inputs (dict): Dictionary containing user inputs for various attributes of the scene.

    Returns:
    - prompt (str): A formatted string that serves as a prompt for video generation.
    """

    # Extract inputs from the dictionary
    camera_style = inputs["Technicalities"]["Camera Style"]
    lighting_style = inputs["Technicalities"]["Lighting Style"]
    movement_speed = inputs["Technicalities"]["Movement Speed"]
    movement_type = inputs["Technicalities"]["Movement Type"]
    style_aesthetic = inputs["Technicalities"]["Style & Aesthetic"]

    environment = inputs["Scene Details"]["Environment"]
    setting_time = inputs["Scene Details"]["Setting (Time of Day)"]
    weather = inputs["Scene Details"]["Weather"]
    scene_lighting = inputs["Scene Details"]["Lighting"]
    subject_attire = inputs["Scene Details"]["Subject Attire"]
    mood = inputs["Scene Details"]["Mood"]

    age = inputs["Subject Description"]["Age"]
    gender = inputs["Subject Description"]["Gender"]
    ethnicity = inputs["Subject Description"]["Ethnicity"]
    emotion = inputs["Subject Description"]["Emotion"]
    positioning = inputs["Subject Description"]["Positioning"]
    physical_appearance = inputs["Subject Description"]["Physical Appearance"]

    storyline = inputs["Storyline"]["Scene/Action Description"]

    style_aesthetic_terms = inputs["Keywords"]["Style & Aesthetic Terms"]
    textures = inputs["Keywords"]["Textures"]
    additional_descriptors = inputs["Keywords"]["Additional Descriptors"]

    # Construct the prompt in a structured format
    prompt = (
        f"**Scene {stage}**: **{camera_style.capitalize()} shot**: {environment} during {setting_time.lower()} "
        f"with {weather.lower()} conditions. The scene is lit with {scene_lighting.lower()}, creating a "
        f"{mood.lower()} atmosphere. {storyline}. The subject, a {age.lower()} {gender.lower()} of "
        f"{ethnicity.lower()} descent, appears {emotion.lower()} and is {positioning.lower()}. "
        f"The subject is dressed in {subject_attire.lower()} and has a physical appearance described as "
        f"{physical_appearance.lower()}. The camera captures the scene with {movement_speed.lower()} movement, "
        f"{movement_type.lower()} through the environment, highlighting {textures.lower()} textures. "
        f"The overall aesthetic is {style_aesthetic.lower()} with elements of {style_aesthetic_terms.lower()}. "
        f"Additional descriptors: {additional_descriptors}."
    )

    return prompt

from langchain_core.messages import AIMessage

def make_prompt_good_for_runwayml(prompt, prev_scene):

    messages = [
        ('system', """

        KEEP THE PROMPT WIthin 500 CHARCATER LEN, no need to use crazy formatting or markdown syntax. SImple text will work
    INSTRUCTIONS FOR WRITING A GOOD PROMPT:
        You are a very intelligent prompt engineer. You help in writing suitable prompts for Runway ML models, following the provided guidelines.

        Guidelines:

        Prompt Structures
        Text-only Base Prompt
        Use a clear structure to divide details about each scene into separate sections, ensuring each scene connects smoothly to the next.

        For generating continuous video clips across different stages of a narrative, use the following structure:

        **Scene [Stage Name]**: [camera movement]: [establishing scene]. [additional details].

        Ensure that each scene is connected logically to the previous one to create a cohesive story.

        Example Prompts for Different Stages:
        - **Introduction**: **Wide-angle shot**: A picturesque village emerges in the early morning light, with mist rolling over the hills. Birds chirp softly in the background.

        - **Inciting Incident**: **Dramatic close-up**: A character's eyes widen in shock as they receive unexpected news, their surroundings blurring out of focus.

        - **Rising Actions**: **Dynamic tracking shot**: The camera follows the protagonist running through a dense forest, the sound of rushing water echoing nearby.

        - **Conflict**: **High-angle shot**: A tense standoff between two characters in a dimly lit alley, shadows casting ominous shapes on the walls.

        - **Climax**: **360-degree rotating shot**: As the battle reaches its peak, the camera spins around the action, capturing the intensity and chaos from all angles.

        - **Resolution**: **Slow pull-back shot**: The camera slowly pulls back from a peaceful sunset, revealing the characters embracing in the foreground, a sense of closure settling in.

        Bracket Placeholders
        For creating reusable custom prompts, place parts of your prompt in brackets for easy replacement.
        Example: Scene **[Stage Name]**: The camera transitions through **[subject location]**.
"""),
(
    "human", f"""
    KEEP THE PROMPT WIthin 500 CHARCATER LEN, number of character less than equal to 500 without losing any necessary details of scene, no need to use crazy formatting or markdown syntax. SImple text will work

        Make my prompt for makeing a video in Runway ML models.

        WHAT THINGS I WANT IN CURRENT SCENE:
        {prompt}

        {f'PREVIOUS SCENE was {prev_scene}' if prev_scene != '' else ''}

    PLEASE GENERATE THE PROMPT, keep the video in conitnutaiton don't keep showing sma ething. Proceed in storyline. FOCUSE ON current scene and keep that details in prompt. Don't mix all in one

    PROMPT THAT SHALL BE SENT TO RUNWAY MODEL THAT YOU MADE SHALL BE ENCLOSED IN <PROMPT>.... </PROMPT>
    """
)

    ]
    ai_msg = llm.invoke(messages)
    message = ai_msg.content

    import re

    # Regular expression to find text between <PROMPT> and </PROMPT>
    pattern = r'<PROMPT>(.*?)</PROMPT>'

    return re.findall(pattern, message, re.DOTALL)[0][:512]

RUNWAYML_API_SECRET="key_bda7f6833abc5475cd5b4f56cc3931e73fb81ed6831cf79bd84e7cbd688ea7324349de13cec293d9ab3aa70220a3047d149212f9a2f6282bd7a23f42fd9fa34f"

import time
from runwayml import RunwayML

client = RunwayML(api_key=RUNWAYML_API_SECRET)

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def video_gen(prompts):
    # Create a new image-to-video task using the "gen3a_turbo" model
    task_ids = []
    completed_tasks = []  # List to store completed tasks

    # Submit tasks concurrently
    with ThreadPoolExecutor() as executor:
        future_to_task = {}

        # Start all tasks and store their future objects
        for prompt in prompts:
            future = executor.submit(client.image_to_video.create,
                                     model='gen3a_turbo',
                                     prompt_image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZNr-JwntYcrRWS4T3iOITBt3jmXA2eGHjiA&s",
                                     prompt_text=prompt)
            future_to_task[future] = prompt

        # Collect task IDs as they complete
        for future in as_completed(future_to_task):
            task = future.result()
            task_ids.append(task.id)
            print(f"Task started for prompt '{future_to_task[future]}', task ID: {task.id}")

    # Poll tasks concurrently until all are complete
    with ThreadPoolExecutor() as executor:
        def poll_task(task_id):
            while True:
                task = client.tasks.retrieve(task_id)
                if task.status in ['SUCCEEDED', 'FAILED']:
                    return task  # Return the completed task
                time.sleep(10)  # Wait for ten seconds before polling

        future_to_task_id = {executor.submit(poll_task, task_id): task_id for task_id in task_ids}

        # Collect completed tasks
        for future in as_completed(future_to_task_id):
            task = future.result()
            completed_tasks.append(task)
            print(f'Task complete for task ID {future_to_task_id[future]}:', task)

    return completed_tasks  # Return the list of completed tasks


def make_prompts(inputs):
    prompts = []
    stages = ["Introduction", "Inciting Incident", "Rising Actions", "Conflict", "Climax", "Resolution"]
    prev_scene = ''
    # Generate prompts for each stage

    for i in range(len(inputs)):
        prompts.append(
            prev_scene := make_prompt_good_for_runwayml(
                create_stage_prompt(stages[i], inputs[i]), prev_scene
            )
        )

    return prompts

def generate_video(scenes_data):
    # This function would generate the video based on all scenes' data
    print(scenes_data)
    prompts = make_prompts(scenes_data)
    videos = video_gen(prompts)
    print(videos)
    output_path = download_videos(videos)
    print(output_path)
    return 'final_video.mp4'

import requests
from moviepy.editor import concatenate_videoclips, VideoFileClip

import requests

def download_v(url, index):
    # Send a GET request to the URL to fetch the video content
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Define the filename with the index as part of the name
        filename = f"video_{index}.mp4"
        
        # Open the file in write-binary mode and save the content
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        print(f"Video saved as {filename}")
    else:
        print(f"Failed to download video from {url}")
        

def download_videos(output_runway):

    video_urls = []

    for output in output_runway:
        video_urls.append(output.output[0])

    # Download videos and store their file paths
    video_files = [download_v(url, i) for i, url in enumerate(video_urls)]

    # Load the downloaded videos using moviepy
    video_clips = [VideoFileClip(file) for file in video_files]

    # Concatenate the video clips
    final_clip = concatenate_videoclips(video_clips, method="compose")

    # Output the final video to a file
    final_clip.write_videofile("final_video.mp4", codec="libx264")

    print("Video concatenation complete. Saved as 'final_video.mp4'.")
    return "final_video.mp4"


import streamlit as st
import json

def initialize_scene_state(scene_name):
    """Initialize default state for a scene if it doesn't exist"""
    if f'scene_{scene_name}' not in st.session_state:
        st.session_state[f'scene_{scene_name}'] = {
            "Technicalities": {
                "Camera Style": "Low angle",
                "Lighting Style": "Diffused lighting",
                "Movement Speed": "Dynamic motion",
                "Movement Type": "Grows",
                "Style & Aesthetic": "Moody",
            },
            "Scene Details": {
                "Environment": "Urban",
                "Setting (Time of Day)": "Dawn",
                "Weather": "Clear",
                "Lighting": "Natural",
                "Subject Attire": "",
                "Mood": "Happy",
            },
            "Subject Description": {
                "Age": "Adult",
                "Gender": "Prefer Not to Specify",
                "Ethnicity": "Mixed/Other",
                "Emotion": "Happy",
                "Positioning": "Standing",
                "Physical Appearance": "",
            },
            "Storyline": {
                "Scene/Action Description": "",
            },
            "Keywords": {
                "Style & Aesthetic Terms": "Moody",
                "Textures": "Smooth",
                "Additional Descriptors": "",
            }
        }

def scene_inputs(scene_name):
    """Create inputs for a scene and store in session state"""
    scene_key = f'scene_{scene_name}'

    # Technicalities
    st.header("Technicalities")
    st.session_state[scene_key]["Technicalities"]["Camera Style"] = st.selectbox(
        "Camera Style",
        ["Low angle", "High angle", "Overhead", "FPV", "Handheld", "Wide angle", "Close up", "Macro cinematography", "Over the shoulder", "Tracking", "Establishing wide", "50mm lens", "SnorriCam", "Realistic documentary", "Camcorder"],
        key=f"{scene_key}_camera_style"
    )
    st.session_state[scene_key]["Technicalities"]["Lighting Style"] = st.selectbox(
        "Lighting Style",
        ["Diffused lighting", "Silhouette", "Lens flare", "Back lit", "Side lit", "Venetian lighting"],
        key=f"{scene_key}_lighting_style"
    )
    st.session_state[scene_key]["Technicalities"]["Movement Speed"] = st.selectbox(
        "Movement Speed",
        ["Dynamic motion", "Slow motion", "Fast motion", "Timelapse"],
        key=f"{scene_key}_movement_speed"
    )
    st.session_state[scene_key]["Technicalities"]["Movement Type"] = st.selectbox(
        "Movement Type",
        ["Grows", "Emerges", "Explodes", "Ascends", "Undulates", "Warps", "Transforms", "Ripples", "Shatters", "Unfolds", "Vortex"],
        key=f"{scene_key}_movement_type"
    )
    st.session_state[scene_key]["Technicalities"]["Style & Aesthetic"] = st.selectbox(
        "Style & Aesthetic",
        ["Moody", "Cinematic", "Iridescent", "Home video VHS", "Glitchcore"],
        key=f"{scene_key}_style_aesthetic"
    )

    # Scene Details
    st.header("Scene Details")
    st.session_state[scene_key]["Scene Details"]["Environment"] = st.selectbox(
        "Environment",
        ["Urban", "Rural", "Suburban", "Wilderness", "Coastal", "Desert", "Mountainous", "Indoor", "Outdoor", "Forest", "Ocean/Beach"],
        key=f"{scene_key}_environment"
    )
    st.session_state[scene_key]["Scene Details"]["Setting (Time of Day)"] = st.selectbox(
        "Setting (Time of Day)",
        ["Dawn", "Morning", "Midday", "Afternoon", "Evening", "Sunset", "Dusk", "Night"],
        key=f"{scene_key}_setting_time"
    )
    st.session_state[scene_key]["Scene Details"]["Weather"] = st.selectbox(
        "Weather",
        ["Clear", "Cloudy", "Rainy", "Snowy", "Foggy", "Stormy", "Windy", "Hazy"],
        key=f"{scene_key}_weather"
    )
    st.session_state[scene_key]["Scene Details"]["Lighting"] = st.selectbox(
        "Lighting",
        ["Natural", "Artificial", "Low Light", "High Key", "Low Key", "Soft Light", "Hard Light"],
        key=f"{scene_key}_scene_lighting"
    )
    st.session_state[scene_key]["Scene Details"]["Subject Attire"] = st.text_input(
        "Subject Attire",
        value=st.session_state[scene_key]["Scene Details"]["Subject Attire"],
        key=f"{scene_key}_subject_attire"
    )
    st.session_state[scene_key]["Scene Details"]["Mood"] = st.selectbox(
        "Mood",
        ["Happy", "Sad", "Tense", "Calm", "Romantic", "Mysterious", "Dramatic", "Fearful", "Excited", "Nostalgic"],
        key=f"{scene_key}_mood"
    )

    # Subject Description
    st.header("Subject Description")
    st.session_state[scene_key]["Subject Description"]["Age"] = st.selectbox(
        "Age",
        ["Child", "Teen", "Young Adult", "Adult", "Middle-Aged", "Elderly"],
        key=f"{scene_key}_age"
    )
    st.session_state[scene_key]["Subject Description"]["Gender"] = st.selectbox(
        "Gender",
        ["Male", "Female", "Non-binary", "Prefer Not to Specify"],
        key=f"{scene_key}_gender"
    )
    st.session_state[scene_key]["Subject Description"]["Ethnicity"] = st.selectbox(
        "Ethnicity",
        ["Asian", "Black", "Hispanic or Latino", "Native American", "White", "Middle Eastern", "Mixed/Other"],
        key=f"{scene_key}_ethnicity"
    )
    st.session_state[scene_key]["Subject Description"]["Emotion"] = st.selectbox(
        "Emotion",
        ["Happy", "Sad", "Angry", "Confused", "Excited", "Anxious", "Calm", "Fearful", "Surprised"],
        key=f"{scene_key}_emotion"
    )
    st.session_state[scene_key]["Subject Description"]["Positioning"] = st.selectbox(
        "Positioning",
        ["Standing", "Sitting", "Lying Down", "Running", "Walking", "Facing Camera", "Profile", "Back to Camera", "Close-Up", "Mid-Shot", "Full Body"],
        key=f"{scene_key}_positioning"
    )
    st.session_state[scene_key]["Subject Description"]["Physical Appearance"] = st.text_input(
        "Physical Appearance",
        value=st.session_state[scene_key]["Subject Description"]["Physical Appearance"],
        key=f"{scene_key}_physical_appearance"
    )

    # Storyline
    st.header("Storyline")
    st.session_state[scene_key]["Storyline"]["Scene/Action Description"] = st.text_area(
        "Scene/Action Description",
        value=st.session_state[scene_key]["Storyline"]["Scene/Action Description"],
        key=f"{scene_key}_scene_action_desc"
    )

    # Keywords
    st.header("Keywords")
    st.session_state[scene_key]["Keywords"]["Style & Aesthetic Terms"] = st.selectbox(
        "Style & Aesthetic Terms",
        ["Moody", "Cinematic", "Iridescent", "Home video VHS", "Glitchcore", "Vintage", "Noir", "Futuristic", "Minimalistic", "Grunge", "Abstract", "Surreal"],
        key=f"{scene_key}_style_aesthetic_terms"
    )
    st.session_state[scene_key]["Keywords"]["Textures"] = st.selectbox(
        "Textures",
        ["Smooth", "Rough", "Glossy", "Matte", "Grainy", "Metallic", "Soft", "Sharp"],
        key=f"{scene_key}_textures"
    )
    st.session_state[scene_key]["Keywords"]["Additional Descriptors"] = st.text_input(
        "Additional Descriptors",
        value=st.session_state[scene_key]["Keywords"]["Additional Descriptors"],
        key=f"{scene_key}_additional_descriptors"
    )


def main():
    st.title("Multi-Scene Video Generation Tool")

    # Initialize session state for all scenes
    scenes = ["Introduction", "Inciting Incident", "Rising Actions", "Conflict", "Climax", "Resolution"]
    for scene in scenes:
        initialize_scene_state(scene)

    # Create tabs for each scene
    tabs = st.tabs(scenes)

    # Display inputs for each scene in its respective tab
    for i, tab in enumerate(tabs):
        with tab:
            st.subheader(f"Scene {i+1}: {scenes[i]}")
            scene_inputs(scenes[i])

    # Generate video button (outside the tabs)
    if st.button("Generate Complete Video"):
        # Collect all scene data
        all_scenes_data = [st.session_state[f'scene_{scene}'] for scene in scenes]
        video_path = generate_video(all_scenes_data)
        st.video(video_path)

        # Provide download option
        st.download_button(
            label="Download Video",
            data=open(video_path, 'rb').read(),
            file_name="generated_video.mp4",
            mime="video/mp4"
        )


if __name__ == "__main__":
    main()

