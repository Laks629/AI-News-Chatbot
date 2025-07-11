from fastapi import FastAPI
from datetime import datetime, timedelta
import mysql.connector

app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lakshminair@2699",
    database="ai_news"
)

@app.get("/headlines")
def get_headlines(days: int = 30):
    cursor = db.cursor(dictionary=True)
    since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    query = "SELECT headline, link, pub_date FROM headlines WHERE pub_date >= %s"
    cursor.execute(query, (since_date,))
    results = cursor.fetchall()
    return results
