SELECT * FROM banks;

SELECT 
    (SELECT COUNT(*) FROM positive_reviews_with_themes) AS positive_count,
    (SELECT COUNT(*) FROM negative_reviews_with_themes) AS negative_count;
-- -- This query retrieves all records from the 'banks' table and counts the number of positive and negative reviews from their respective tables.

SELECT bank_name, COUNT(*) AS total_reviews
FROM positive_reviews_with_themes
GROUP BY bank_name
ORDER BY total_reviews DESC;
-- This query counts the total number of positive reviews for each bank and orders the results in descending order.

SELECT bank_name, COUNT(*) AS total_reviews
FROM negative_reviews_with_themes
GROUP BY bank_name
ORDER BY total_reviews DESC;

-- This query counts the total number of negative reviews for each bank and orders the results in descending order.


SELECT bank_name, ROUND(AVG(rating), 2) AS avg_rating
FROM positive_reviews_with_themes
GROUP BY bank_name
ORDER BY avg_rating DESC;
-- This query calculates the average rating for each bank based on positive reviews and orders the results in descending order.


SELECT 
    SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) AS missing_review_text,
    SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END) AS missing_rating,
    SUM(CASE WHEN review_date IS NULL THEN 1 ELSE 0 END) AS missing_review_date
FROM positive_reviews_with_themes;
-- This query checks for missing values in critical fields of the positive reviews table.


SELECT sentiment_group, COUNT(*) AS total
FROM positive_reviews_with_themes
GROUP BY sentiment_group;
-- This query groups positive reviews by sentiment group and counts the total number in each group.

SELECT sentiment_group, COUNT(*) AS total
FROM negative_reviews_with_themes
GROUP BY sentiment_group;

-- This query groups negative reviews by sentiment group and counts the total number in each group. 


SELECT bank_name, theme, COUNT(*) AS total
FROM positive_reviews_with_themes
GROUP BY bank_name, theme
ORDER BY bank_name, total DESC;
-- This query counts the occurrences of each theme in positive reviews for each bank and orders the results by bank name and total count.

SELECT 
    MIN(review_date) AS earliest_review,
    MAX(review_date) AS latest_review
FROM positive_reviews_with_themes;
-- This query finds the earliest and latest review dates in the positive reviews table.
