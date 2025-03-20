from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from hebrew_w2v_api import HebrewSimilarWords

import random
import os
import gdown

# SETUP:
if not os.path.exists("./wiki-w2v/words_vectors.npy"):
    fileID = "13ag2AoEf7s5GUyQMSBJ4HMsuZ8sS_3SL"
    outputFile = "wiki-w2v/words_vectors.npy"
    gdown.download(f"https://drive.google.com/uc?id={fileID}", outputFile, quiet=False)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "https://orijer.github.io/GuessTheWordFrontend/"], 
                   allow_credentials=True, allow_methods=["GET"], allow_headers=["*"])
model = HebrewSimilarWords()

f = open("words.txt", "r", encoding="utf-8")
words = f.readlines()
f.close()

# UTILITY FUNCTIONS:
def get_hidden_word(id):
    if id < 0:
        raise HTTPException(status_code=400, detail="id must be non-negative.")
    
    return words[id % len(words)].strip()

def get_hint(word):
    hints = [
        f"המילה הסודית מתחילה באות '{word[0]}'",
        f"המילה הסודית מסתיימת באות '{word[-1]}'",
        f"המילה הסודית מכילה '{len(word)}' אותיות",
        f"המילה הסודית מכילה את האות '{random.choice(word)}'"
    ]
    
    closest_words = model.get_most_similar(word)[5:]
    for close_word in closest_words:
        hints.append(f"המילה '{close_word["word"]}' קרובה למילה הסודית")
    
    return random.choice(hints)

# API:
@app.get("/eval/{id}/{word}")
def eval_word(id: int, word: str):
    hidden_word = get_hidden_word(id)
    try:
        return {"similarity" : model.calc_similarity(hidden_word, word)[2]}
    except:
        raise HTTPException(status_code=400, detail=word+" doesn't exist in the vocabulary.")

@app.get("/hint/{id}")
def hint(id: int):
    hidden_word = get_hidden_word(id)
    return {"hint" : get_hint(hidden_word)}
    
# Run command: python -m uvicorn server:app --host 0.0.0.0 --port 8000