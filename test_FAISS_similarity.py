#This code is just for learning purpose to check that FAISS inner product == manual cosine similarity

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss

# Load CSV
df = pd.read_csv('news_scrape.csv')

# Load the same model 
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load  embeddings from file if you saved them,
# here we re-encode for a simple test:
embeddings = np.vstack(df['Headline'].apply(lambda x: model.encode(x, normalize_embeddings=True)).to_list()).astype('float32')

# Build FAISS index (inner product == cosine if normalized)
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

# Pick a test query
query = "AI in agriculture"
query_emb = model.encode(query, normalize_embeddings=True).astype('float32').reshape(1, -1)

# Get top result from FAISS
D, I = index.search(query_emb, k=1)
faiss_score = D[0][0]
top_idx = I[0][0]

print(f"🔎 FAISS says: top match = {df.iloc[top_idx]['Headline']}")
print(f"FAISS cosine score: {faiss_score:.4f}")

# 7) Manual cosine for same pair
manual_score = float(np.dot(query_emb, embeddings[top_idx])) / (
    np.linalg.norm(query_emb) * np.linalg.norm(embeddings[top_idx])
)

print(f"Manual cosine similarity: {manual_score:.4f}")

# 8) Check difference
diff = abs(faiss_score - manual_score)
print(f"Difference: {diff:.8f} (should be ~0)")
