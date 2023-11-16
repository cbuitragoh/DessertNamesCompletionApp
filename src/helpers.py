from transformers import pipeline, set_seed
import openai
import json
from PIL import Image
import requests
import re
import os
import unicodedata


# general variables
openAI_models = ["gpt-4-0314", "gpt-3.5-turbo-0613"]   
huggingface_models = ["openai-gpt"] 


# load base image app
def load_base_image(image_path: str = "./media/dessert.jpg") -> Image:
    image = Image.open(image_path)
    return image


#load examples and setting prompt
def load_base_messages() -> list:
    with open("src/examples.json", "r") as f:
        data_prompt = json.load(f)
        base_messages = data_prompt["examples"]
    return base_messages


# Normalize text
def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    text = text.strip()
    return text


# function to create generator
def create_generator(
        prompt: str,
        seed: int,
        openai_api_key: str | None,
        model: str = "openai-gpt"
    ) -> str:
    """ This function makes calls to a huggingFace model
        or openAI models to generate dessert suggestion
        names based on user input.
    """

    if model in openAI_models:
        openai.api_key = openai_api_key
        messages = load_base_messages()
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=50,
            temperature=0
        )
        return response["choices"][0]["message"]["content"]
    else:
        generator = pipeline('text-generation', model=model)
        set_seed(seed)
        results = generator(prompt, max_length=15, num_return_sequences=1)
        if results:
            return results[0]['generated_text']
        else:
            return "Sorry something is wrong!"


# function to generate images from Dalle-3 OpenAI
async def generate_dessert_image(dessert_name:str, openai_api_key:str) -> str:
    openai.api_key = openai_api_key
    response = openai.Image.create(
        prompt=f"{dessert_name}",
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']


# function to show image
def show_image(image_url:str) -> Image:
    image = Image.open(requests.get(image_url, stream=True).raw)
    return image

# function to save image
def save_tempImage(PIL_image:Image.Image, image_name:str):
    image_path = f"src/tempImages/{image_name}.jpg"
    if not os.path.exists("src/tempImages"):
        os.mkdir("src/tempImages")
        PIL_image.save(image_path)
    else:
        PIL_image.save(image_path)

    return image_path

# function to delete temporal image 
def del_tempImage(image_path:str):
    os.remove(image_path)