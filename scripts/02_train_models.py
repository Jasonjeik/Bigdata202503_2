# scripts/02_train_models.py 

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.BDProyecto2

# -----------------------------
# 1. Modelo de Recomendación NCF con PyTorch
# -----------------------------
print("Entrenando modelo de recomendación NCF...")

ratings = pd.DataFrame(list(db.ratings.find({}, {"userId":1, "movieId":1, "rating":1})))
user_enc = LabelEncoder()
movie_enc = LabelEncoder()
ratings['user'] = user_enc.fit_transform(ratings['userId'])
ratings['movie'] = movie_enc.fit_transform(ratings['movieId'])
n_users = ratings['user'].nunique()
n_movies = ratings['movie'].nunique()

class MovieLensDataset(Dataset):
    def __init__(self, users, movies, ratings):
        self.users = torch.tensor(users, dtype=torch.long)
        self.movies = torch.tensor(movies, dtype=torch.long)
        self.ratings = torch.tensor(ratings, dtype=torch.float)
    def __len__(self): return len(self.users)
    def __getitem__(self, idx):
        return self.users[idx], self.movies[idx], self.ratings[idx]

train_users, test_users, train_movies, test_movies, train_ratings, test_ratings = train_test_split(
    ratings['user'].values, ratings['movie'].values, ratings['rating'].values, test_size=0.2, random_state=42)

train_dataset = MovieLensDataset(train_users, train_movies, train_ratings)
train_loader = DataLoader(train_dataset, batch_size=1024, shuffle=True)

class NCF(nn.Module):
    def __init__(self, n_users, n_movies, embed_size=64, layers=[128, 64, 32, 16]):
        super().__init__()
        self.user_emb = nn.Embedding(n_users, embed_size)
        self.movie_emb = nn.Embedding(n_movies, embed_size)
        layers = [embed_size*2] + layers + [1]
        self.mlp = nn.Sequential()
        for i in range(len(layers)-1):
            self.mlp.add_module(f"linear{i}", nn.Linear(layers[i], layers[i+1]))
            if i < len(layers)-2:
                self.mlp.add_module(f"relu{i}", nn.ReLU())
    def forward(self, user, movie):
        u = self.user_emb(user)
        m = self.movie_emb(movie)
        x = torch.cat([u, m], dim=1)
        return self.mlp(x).squeeze()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_ncf = NCF(n_users, n_movies).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model_ncf.parameters(), lr=0.001)

for epoch in range(5):  # 5 épocas bastan para demo perfecta
    model_ncf.train()
    total_loss = 0
    for user, movie, rating in tqdm(train_loader, desc=f"Epoch {epoch+1}/5"):
        user, movie, rating = user.to(device), movie.to(device), rating.to(device)
        pred = model_ncf(user, movie)
        loss = criterion(pred, rating)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1} - Loss: {total_loss/len(train_loader):.4f}")

# Guardar modelo recomendación
torch.save({
    'model_state_dict': model_ncf.state_dict(),
    'user_encoder': user_enc,
    'movie_encoder': movie_enc,
    'n_users': n_users,
    'n_movies': n_movies
}, "api/models/ncf_recommendation.pth")
print("Modelo NCF guardado")

# -----------------------------
# 2. Modelo Sentiment Analysis (LSTM) con PyTorch
# -----------------------------
print("Entrenando modelo de Sentiment Analysis...")

from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
import re

reviews = pd.DataFrame(list(db.reviews.find()))
tokenizer = get_tokenizer('basic_english')

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text.strip()

reviews['tokens'] = reviews['review'].apply(lambda x: tokenizer(clean_text(x)))
vocab = build_vocab_from_iterator(reviews['tokens'], specials=['<unk>', '<pad>'])
vocab.set_default_index(vocab['<unk>'])

class ReviewDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_len=200):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_len = max_len
    def __len__(self): return len(self.texts)
    def __getitem__(self, idx):
        tokens = self.texts[idx][:self.max_len]
        seq = [self.vocab[t] for t in tokens]
        if len(seq) < self.max_len:
            seq += [self.vocab['<pad>']] * (self.max_len - len(seq))
        return torch.tensor(seq), torch.tensor(self.labels[idx], dtype=torch.long)

train_texts, test_texts, train_labels, test_labels = train_test_split(
    reviews['tokens'], reviews['sentiment'], test_size=0.2, random_state=42)

train_ds = ReviewDataset(train_texts.tolist(), train_labels.tolist(), vocab)
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)

class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embed_size=128, hidden_size=256):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size, padding_idx=vocab['<pad>'])
        self.lstm = nn.LSTM(embed_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 2)
    def forward(self, x):
        x = self.embedding(x)
        _, (h_n, _) = self.lstm(x)
        return self.fc(h_n.squeeze(0))

model_sentiment = SentimentLSTM(len(vocab)).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model_sentiment.parameters(), lr=0.001)

for epoch in range(6):
    model_sentiment.train()
    for seq, label in tqdm(train_loader, desc=f"Sentiment Epoch {epoch+1}/6"):
        seq, label = seq.to(device), label.to(device)
        pred = model_sentiment(seq)
        loss = criterion(pred, label)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

torch.save(model_sentiment.state_dict(), "api/models/sentiment_lstm.pth")
torch.save(vocab, "api/models/vocab.pth")
print("Modelo Sentiment guardado")

print("¡TODOS LOS MODELOS ENTRENADOS Y GUARDADOS!")