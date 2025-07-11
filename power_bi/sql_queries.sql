/* Articles per month*/
CREATE OR REPLACE VIEW articles_trend AS
SELECT pub_date, COUNT(*) AS total_articles
FROM headlines
GROUP BY pub_date
ORDER BY pub_date;


/* Top count (6 months)*/
CREATE OR REPLACE VIEW top_keyword AS
SELECT keyword, count
FROM keywords
ORDER BY count DESC
LIMIT 50;


/* latest headlines */

CREATE OR REPLACE VIEW latest_feed AS
SELECT headline, link, pub_date
FROM headlines
ORDER BY pub_date DESC
LIMIT 20;

