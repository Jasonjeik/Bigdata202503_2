import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client.BDProyecto2

# 1. Cargar películas
movies = pd.read_csv("data/ml-25m/movies.csv")
movies_dict = movies.to_dict("records")
db.movies.drop()
db.movies.insert_many(movies_dict)
print("Películas cargadas:", db.movies.count_documents({}))

# 2. Cargar ratings (25 millones en lotes)
ratings = pd.read_csv("data/ml-25m/ratings.csv")
batch_size = 10000
for i in range(0, len(ratings), batch_size):
    batch = ratings[i:i+batch_size].to_dict("records")
    db.ratings.insert_many(batch)
    print(f"Cargado {i+batch_size}/{len(ratings)} ratings")

# 3. Cargar reviews IMDB (sentiment)
reviews = pd.read_csv("data/IMDB Dataset.csv")
reviews = reviews.head(20000)  # 20k bastan para entrenar rápido
reviews["sentiment"] = reviews["sentiment"].map({"positive": 1, "negative": 0})
reviews_dict = reviews.to_dict("records")
db.reviews.drop()
db.reviews.insert_many(reviews_dict)
print("Reviews cargadas")