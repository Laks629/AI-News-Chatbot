import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lakshminair@2699",
    database="ai_news"
)
cursor = db.cursor()

source = "https://techcrunch.com/category/artificial-intelligence/"
seen = set()

while True:
    response = requests.get(source)
    soup = BeautifulSoup(response.text, "lxml")

    articles = soup.find_all("li", class_="wp-block-post")

    if not articles:
        break

    for article in articles:
        headline_tag = article.find("a", class_="loop-card__title-link")
        date_tag = article.find("time", class_=lambda x: x and "loop-card__meta-item" in x)
    
        if date_tag and date_tag.has_attr('datetime'):
            date = date_tag['datetime']        
            

        if headline_tag:
            headline = headline_tag.get_text(strip=True)
            link = headline_tag['href']

        unique_key = (headline, link)
        if unique_key not in seen:
            seen.add(unique_key)

            # Insert into DB
            sql = "INSERT IGNORE INTO headlines (headline, link, pub_date) VALUES (%s, %s, %s)"
            val = (headline, link, date)
            cursor.execute(sql, val)

    # Find next page
    next_page = soup.find("a", class_="wp-block-query-pagination-next")
    if next_page and next_page.has_attr('href'):
        source = next_page["href"]
    else:
        break

db.commit()
cursor.close()
db.close()
print("Scrape complete! Saved to MySQL.")
