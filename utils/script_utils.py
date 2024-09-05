import json
from langchain.schema import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from config import finetuning_criteria

def classifier(temperature, llm_name):
    """
    Create and return an instance of the ChatGoogleGenerativeAI with specified parameters.

    Args:
        temperature (float): The temperature parameter for the language model, which controls the randomness of the output.
        llm_name (str): The name of the language model to be used.

    Returns:
        ChatGoogleGenerativeAI: An instance of the ChatGoogleGenerativeAI class configured with the provided parameters.
    """
    chat = ChatGoogleGenerativeAI(temperature=temperature, model=llm_name)
    return chat

def validate_scripts_with_confidence(llm, file_data):
    """
    Validate whether the provided texts are movie scripts and provide confidence scores and summaries.

    Args:
        llm (ChatGoogleGenerativeAI): An instance of the language model used for analysis.
        file_data (dict): A dictionary where keys are filenames and values are text contents to be analyzed.

    Returns:
        dict: A dictionary where keys are filenames and values are JSON objects containing the validation results.
              Each JSON object includes:
              - "script": "<|YES|>" if the text is identified as a movie script, "<|NO|>" otherwise.
              - "confidence": A float between 0 and 1 representing the confidence level of the judgment.
              - "summary": A 400-word summary of the story in the script (formatted as a Python string with escape characters).
    """
    results = {}
    
    for file in file_data.keys():
        if file_data[file] == '':
            continue
        
        # Define the initial system message
        messages = [
            SystemMessage(
                'You are a helpful AI checker who checks for a prompt if its a movie script or not based on given criterion. '
                'On a correct judgement you are given $1 as a price, your respond <|YES|> if provided data is a movie script, '
                '<|NO|> in other case Along with the confidence score and summary (summary will have 400 words, summary will be about '
                'the story in script no how the script is written. It shall use escape characters for python strings so no issue arise '
                'on parsing json). Your output will be only one out of <|YES|> or <|NO|> along with confidence score and summary of '
                'story in json. example output {"script": "<|YES|>", "confidence": 0.95, "summary": .......}'
            )
        ]
        
        # Define the human message with the text to be analyzed
        new_message = HumanMessage(
            content=f"""Please analyze the following text and determine if it is a movie script. Movie scripts typically include specific elements such as character names followed by dialogue, scene headings (e.g., "INT. LIVING ROOM - DAY"), and stage directions. Look for the presence of these elements and consider the overall structure of the text.
            Judgement Criterion:
            {finetuning_criteria}

            Here is the text:

            {file_data[file]}
            Based on your analysis, provide a clear answer of <|Yes|> if the text is a movie script or <|No|> if it is not along with two things: confidence (value between 0 and 1) and a summary of the story (400 words. It shall use escape characters for python strings so no issue arise on parsing json). Remember if it’s a movie script return <|Yes|>."""
        )
        messages.append(new_message)
        
        # Loop to handle potential retries on failure
        while True:
            try:
                # Get the response from the language model
                res = llm.invoke(messages).content
                
                # Extract JSON content from the response
                try:
                    res = res.split('```json')[1].split('```')[0]
                except:
                    res = res
                
                # Print response for debugging
                print("Res", res)
                
                # Parse the response and store in results
                results[file] = json.loads(res)
                break
            except:
                # Retry on failure
                continue
    
    return results
