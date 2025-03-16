from fastapi import FastAPI, HTTPException
from hebrew_w2v_api import HebrewSimilarWords

app = FastAPI()
model = HebrewSimilarWords()

f = open("words.txt", "r")
words = f.readlines()
f.close()

def get_hidden_word(id):
    if id < 0:
        raise HTTPException(status_code=400, detail="id must be non-negative")
    
    return words[id % len(words)]

@app.get("/eval/{id}/{word}")
def read_root(id: int, word: str):
    hidden_word = get_hidden_word(id)
    return {"similarity" : model.calc_similarity(hidden_word, word)[2]}

# Run command: python -m uvicorn server:app --host 0.0.0.0 --port 8000