import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import dateutil.parser

st.title("AI News Chatbot")

# Load data & index
df = pd.read_parquet("headlines.parquet")
index = faiss.read_index("news.index")


# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')


query = st.text_input("🔎 Ask about latest AI trends (e.g. 'AI in agriculture')")

if query:
    query_emb = model.encode(query, normalize_embeddings=True).astype('float32').reshape(1, -1)
    # Search top 5
    scores, indices = index.search(query_emb, k=5) #cosine similairty 

    st.write(f"## Top matches for: *{query}*")

    for i, idx in enumerate(indices[0]):
        headline = df.iloc[idx]['Headline']
        link = df.iloc[idx]['Link']
        raw_date = df.iloc[idx]['Date']

        try:
            dt = dateutil.parser.parse(raw_date)
            date = dt.strftime("%b %d, %Y")
        except:
            date = raw_date

        st.write(f"{i+1}. [{headline}]({link}) — *{date}*")
