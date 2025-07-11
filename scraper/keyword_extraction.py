import pandas as pd
from collections import Counter
from wordcloud import STOPWORDS
import re
import mysql.connector

#  Connect to DB
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lakshminair@2699",
    database="ai_news"
)
cursor = db.cursor()

# Pull all headlines INTO a DataFrame
df_headlines = pd.read_sql("SELECT headline FROM headlines", con=db)

#Combine headlines & clean punctuation
text = " ".join(df_headlines['headline'].dropna().tolist())
text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation

#Custom stop words

CUSTOM_STOPWORDS = set(['new', 'will', 'now', 'help', 'app', 'use', 'get'])

# Split words & filter
cleaned_words = []
for word in text.split():
    word = word.lower()

    if word in STOPWORDS or word in CUSTOM_STOPWORDS:
        continue  # Remove stopwords

    if word.isdigit():
        continue  # Remove pure numbers like '2024'

    if len(word) < 3:
        continue  # Remove very short junk like 'm' or 'b'

    if re.match(r'^[\d]+[a-z]*$', word):
        continue  # Remove number-unit mix like '50m', '500k', '52b'

    cleaned_words.append(word)


#  Count frequency
word_freq = Counter(cleaned_words)

#Preview top keywords
df_keywords = pd.DataFrame(word_freq.items(), columns=['keyword', 'count'])
print(df_keywords.sort_values('count', ascending=False).head(20))


#  Create keywords table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS keywords (
    keyword VARCHAR(255) PRIMARY KEY,
    count INT
)
""")

#  Insert each keyword with mysql.connector
for _, row in df_keywords.iterrows():
    sql = """
    INSERT INTO keywords (keyword, count)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE count = VALUES(count)
    """
    val = (row['keyword'], int(row['count']))
    cursor.execute(sql, val)

db.commit()
cursor.close()
db.close()

print("Keywords stored in `keywords` table!")
