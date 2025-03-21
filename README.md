# Guess The Word Backend
This repository holds the backend code for my Guess the word game. It uses REST API structure.
In the game there is a secret word that the player needs to find by asking how similar the guess and hidden words are to each other.

# Code
I used FastAPI for the server itself, ontop of a word2vec implementation in hebrew from [here](https://github.com/Ronshm/hebrew-word2vec).
The vector embeddings are to big to store in github, so I saved them on google drive [here](https://drive.google.com/uc?id=13ag2AoEf7s5GUyQMSBJ4HMsuZ8sS_3SL) and I download them during the run using gdown.

In order to run the server locally use: `python -m uvicorn server:app --host 0.0.0.0 --port 8000` (you may swap the port for any available port you'd like).

# API
### GET Similarity:
Get the similarity of a given word to a secret word of a certain id.

Use:  `/eval/id/word`

Return: If the given word is in the vocabulary of the word2vec model, returns {"similarity":val} where similarity is some float number with up to 2 digits after the dot. 
If the given word is not in the vocabulary, returns an exception with status code 400.

### GET Hint:
Get a hint about a secret word of a certain id, like how many letters it had, a hint about a letter it has, similar words to it, and more.

Use: `hint/id`

Return: {"hint": H}, where H is some kind of hint about the word with the id above.

# Host
I am currently hosting this server on render using their free tier, which works great most of the time, but it may be slow for the first interaction.

