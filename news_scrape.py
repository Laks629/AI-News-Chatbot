from bs4 import BeautifulSoup
import requests
import csv
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

source= 'https://techcrunch.com/category/artificial-intelligence/'

# Load existing data if available
if os.path.exists('headlines.parquet'):
    df_old = pd.read_parquet('headlines.parquet')
    print(f"📚 Loaded existing {len(df_old)} headlines")
else:
    df_old = pd.DataFrame(columns=['Headline', 'Link', 'Date'])

seen = set(zip(df_old['Headline'], df_old['Link'])) #for dedupe
new_articles = []
page_count = 1



while True:

    response = requests.get(source)
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all articles

    articles = soup.find_all("li", class_="wp-block-post") 

    if not articles:
        break


    for article in articles:
        headline_tag = article.find("a", class_="loop-card__title-link")
        date_tag = article.find("time", class_=lambda x: x and "loop-card__meta-item" in x)
    # 2. If no <time>, fallback to text inside <ul> or <li>
        if date_tag and date_tag.has_attr('datetime'):
            date = date_tag['datetime']        
            

        if headline_tag:
            headline = headline_tag.get_text(strip=True)
            link = headline_tag['href']

        unique_key = (headline, link)
        if unique_key not in seen:
            seen.add(unique_key)
            new_articles.append({'Headline': headline, 'Link': link, 'Date': date})
            print(f"✅ NEW: {headline}")
            

        

    # Check for Next page button
    next_page = soup.find("a", class_="wp-block-query-pagination-next")

    if next_page and next_page.has_attr('href'):
        source= next_page["href"]
        page_count += 1
    
    else:
        print("No more pages found. Done!")
        break


# Merge & save if needed
if new_articles:
    df_new = pd.DataFrame(new_articles)
    df_final = pd.concat([df_old, df_new]).drop_duplicates(subset=['Headline', 'Link']).reset_index(drop=True)

    # Save CSV & Parquet
    df_final.to_csv('news_scrape.csv', index=False, encoding='utf-8')
    df_final.to_parquet('headlines.parquet', index=False)

    # Generate embeddings & update FAISS
    embeddings = model.encode(df_final['Headline'].tolist(), normalize_embeddings=True).astype('float32')
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, 'news.index')

    print("\n✅ Saved: headlines.parquet, news_scrape.csv, news.index")
else:
    print("\n✅ No new articles found — everything is up to date.")








