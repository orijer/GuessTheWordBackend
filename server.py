from fastapi import FastAPI, HTTPException
from hebrew_w2v_api import HebrewSimilarWords
import gdown
import os

if not os.path.exists("./wiki-w2v/words_vectors.npy"):
    fileID = "13ag2AoEf7s5GUyQMSBJ4HMsuZ8sS_3SL"
    outputFile = "wiki-w2v/words_vectors.npy"
    gdown.download(f"https://drive.google.com/uc?id={fileID}", outputFile, quiet=False)

app = FastAPI()
model = HebrewSimilarWords()

f = open("words.txt", "r", encoding="utf-8")
words = f.readlines()
f.close()

def get_hidden_word(id):
    if id < 0:
        raise HTTPException(status_code=400, detail="id must be non-negative")
    
    return words[id % len(words)].strip()

@app.get("/eval/{id}/{word}")
def read_root(id: int, word: str):
    hidden_word = get_hidden_word(id)
    return {"similarity" : model.calc_similarity(hidden_word, word)[2]}

# Run command: python -m uvicorn server:app --host 0.0.0.0 --port 8000