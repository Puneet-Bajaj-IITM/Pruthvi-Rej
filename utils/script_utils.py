import json
from langchain.schema import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from config import finetuning_criteria


def classifier(temperature, llm_name):
    chat = ChatGoogleGenerativeAI(temperature=temperature,  model=llm_name)
    return chat


def validate_scripts_with_confidence(llm, file_data):
    d = {}
    for file in file_data.keys():
        if file_data[file] == '':
            continue
        messages = [
            SystemMessage("You are a helpful AI checker who checks for a prompt if its a movie script or not based on given criterion. On a correct judgement you are given $1 as a price, your respond <|YES|> if provided data is a movie script, <|NO|> in other case Along with the confidence score. Your output will be only one out of <|YES|> or <|NO|> along with confidence score in json. example output {'script': '<|YES|>', 'confidence': 0.95}")
        ]
        new_message = HumanMessage(
            content=f"""Please analyze the following text and determine if it is a movie script. Movie scripts typically include specific elements such as character names followed by dialogue, scene headings (e.g., "INT. LIVING ROOM - DAY"), and stage directions. Look for the presence of these elements and consider the overall structure of the text.
            Judgement Criterion:
            {finetuning_criteria}

            Here is the text:

            {file_data[file]}
            Based on your analysis, provide a clear answer of <|Yes|> if the text is a movie script or <|No|> if it is not along with confidence value between 0 and 1. Remember if its a movie script return <|Yes|> """
        )
        messages.append(new_message)
        res = llm.invoke(messages).content
        try:
            res = res.split('```json')[1].split('```')[0].replace("'", '"')
        except:
            res = res
        res = res.replace("'", '"')
        d[file] = json.loads(res)
    return d

