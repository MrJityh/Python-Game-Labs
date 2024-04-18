import ollama
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

#paragraph but as a list of sentences
paragraph = [
    "In the vast expanse of space, stars twinkle like distant beacons of light, each one a sun in its own right.", 
    "Planets orbit these stars, some barren and lifeless, while others teem with the bustle of civilizations.", 
    "Among these celestial bodies, asteroids and comets roam, remnants of the early solar system's formation.", 
    "Deep within the cosmic darkness, black holes lurk, their gravitational pull so strong that not even light can escape.",
    "Astronomers tirelessly study these phenomena, unlocking the secrets of the universe.",
    "Space exploration continues to push the boundaries of human knowledge, as we reach out to touch the stars and uncover the mysteries of the cosmos."
    ]
#embed each sentence of the above paragraph
sentenceEmbeddings = []
for sentence in paragraph:
    sentenceEmbeddings.append(ollama.embeddings(model='llama2', prompt=f'{sentence}')['embedding'])

#get input
input_text = input("What's your query?: ")
inputEmbedding = ollama.embeddings(model='llama2', prompt=f'{input_text}')['embedding']

#cosine for simuliarities
similarityList = []
for embedding in sentenceEmbeddings:
    similarity = cosine_similarity([inputEmbedding],[embedding])
    similarityList.append(float(similarity))

#combine and sort by similarities
combined_data = list(zip(paragraph, similarityList))
sorted_data = sorted(combined_data, key=lambda x: x[1], reverse=True)
sorted_sentences = [item[0] for item in sorted_data]
sorted_numbers = [item[1] for item in sorted_data]

#make the context of the query prompt
contextSentence = ""
for i in range(3):
    contextSentence += sorted_sentences[i]
    contextSentence += " "
#form the whole prompt, then generate a response and print
query = contextSentence + " " + input_text 
response = ollama.generate(model='llama2', prompt=query)
print(response['response'])