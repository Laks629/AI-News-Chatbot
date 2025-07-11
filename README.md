# AI News Trend Chatbot

This is a prototype semantic search chatbot that scrapes AI news headlines, stores them in a MySQL database, exposes them through a FastAPI, and enables natural language semantic search via a Streamlit app. It also connects to Power BI for dashboarding and trend analysis.

---

## **Project Goal**
Stay updated with the latest AI news by searching thousands of headlines with real-time semantic matching, while also exploring trends and keyword patterns using Power BI dashboards.

---

## **How it works**

1. **Web Scraper (`news_scrape.py`)**
   - Scrapes AI-related headlines from TechCrunch.
   - Saves headline, link, and publish date to a MySQL database.
   - Optionally updates a local .csv or .parquet file for backup.

2. **FastAPI (api_chatbot.py)**
   - Provides a REST endpoint /headlines?days=30 to pull the latest headlines from MySQL.
   - Filters data dynamically for the Streamlit chatbot and for Power BI ETL.

3. **Semantic Search (chatbot.py)**
   - Loads latest headlines using the FastAPI endpoint.
   - Generates embeddings with a pre-trained SentenceTransformer (all-MiniLM-L6-v2).
   - Uses FAISS for fast semantic similarity search on the fly.
   - Displays matching headlines in an interactive Streamlit interface.

4. **Frontend**
   - Runs in **Streamlit** for a simple chatbot-style query UI.
   - Displays headlines + direct links + publish dates.

5. Power BI Dashboard (powerbi/)
   - Connects to the same MySQL database.
   - Visualizes articles released by TechCrunch (yearly/ quarterly/ monthly) and the freshest headlines for insights. 

---

## **Accuracy**

- **Average relevance score:** `0.78` (out of 1.0)  
- **Precision@5:** ~80% for most queries.
- Covers **direct queries**, **broad queries**, and **ambiguous cases** (`XAI`, `Smart toys`).
- Full details: see [`accuracy_report.md`](./accuracy_report.md) and [`accuracy_report.xlsx`](./accuracy_report.xlsx)

---

## Demo Screenshot

### 🔹 Chatbot UI
![Chatbot UI](./screenshots/chatbot_ui.png)

### 🔹 Accuracy Report
![Accuracy Report](./screenshots/accuracy_report.png)


## **Key folders & files**

| File | Purpose |
|------|---------|
| `scraper/news_scrape.py` | Scrapes headlines, deduplicates, saves to MySQL |
| `scraper/keyword_extraction.py` | Extracts keywords for Power BI trends |
| `api_chatbot.py` | REST API for retrieving latest headlines |
| `chatbot.py` | Streamlit app for user queries |
| `power_bi/news_count.pbix` | Power BI project file |
| `news.index` | Saved `FAISS` index for fast similarity search |
| `accuracy_report.xlsx` | Manual test results with relevance scoring |
| `accuracy_report.md` | Summary of search accuracy |
| `requirements.txt` | Python dependencies |
| `screenshots/` | Screenshots for README |

---

## **How to run**

```bash
# Install Python dependencies
pip install -r requirements.txt

# Scrape and store headlines
python scraper/news_scrape.py

# Run API server
uvicorn api_chatbot:app --reload

# Launch chatbot UI
streamlit run chatbot.py

```

## **What’s next**

- Add longer article snippets for richer context to improve semantic matching.
- Expand the source beyond TechCrunch to cover broader AI industry updates.
- Integrate user feedback signals -e.g., clicks to fine-tune similarity(improve matching) over time.
- Add keyword extraction and NER for deeper insights.
- Add Power BI embed link in the Streamlit chatbot for seamless navigation.
