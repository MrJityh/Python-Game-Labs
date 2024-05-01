import requests
import random
import re

API_TOKEN = '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'
API_URL  = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json={"inputs": payload})
    return response.json

def generate_paragraph(prompt, target_length=10):
    paragraph = ""
    while len(paragraph) < target_length:
        response = query(prompt)
        paragraph += str(response)
        prompt = paragraph[-200:]
    new_text = paragraph[20]
    new_text = new_text.rstrip("'}]")
    
    return new_text

def battle_log():
    options=[
        "Let this be the hour when we draw swords together",
        "Fell deeds awake",
        "Now for wrath, now for ruin, and the red dawn",
        "I do not love the bright sword for its sharpness, I love only what it defends",
        "There's some good in this world, and it's worth fighting or"
    ]
    return generate_paragraph(options[random.randint(0,5)])