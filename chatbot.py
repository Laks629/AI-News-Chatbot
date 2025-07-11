import streamlit as st
import requests
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')

# call the API
response = requests.get("http://127.0.0.1:8000/headlines")
data = response.json()


if not data:
    st.error("No headlines found.")
    st.stop()

# encoding headlines 

df = pd.DataFrame(data)

embeddings = np.vstack(
    df['headline'].apply(lambda x: model.encode(x, normalize_embeddings=True)).to_list()
).astype('float32')

# FAISS index
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

# Streamlit UI 
st.title("AI Latest News Chatbot")
st.write("Ask about AI News")

query = st.text_input("Your Query:")

if query:
    query_emb = model.encode(query, normalize_embeddings=True).astype('float32').reshape(1, -1)
    D, I = index.search(query_emb, k=5)

    st.subheader(f"Top matches for: *{query}*")
    for idx, score in zip(I[0], D[0]):
        headline = df.iloc[idx]['headline']
        link = df.iloc[idx]['link']
        date = df.iloc[idx]['pub_date']
        st.write(f"- [{headline}]({link}) — *{date}*")
