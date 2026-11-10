SELECT
    Market,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    MIN(Modal_Price) AS Minimum_Price,
    MAX(Modal_Price) AS Maximum_Price
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Market
HAVING COUNT(*) >= 10
ORDER BY Average_Modal_Price DESC;

SELECT
    EXTRACT(MONTH FROM Arrival_Date) AS Month_Number,
    FORMAT_DATE('%B', Arrival_Date) AS Month_Name,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    MIN(Modal_Price) AS Minimum_Price,
    MAX(Modal_Price) AS Maximum_Price,
    COUNT(*) AS Total_Records
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Month_Number, Month_Name
ORDER BY Month_Number;

SELECT
    Grade,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    MIN(Modal_Price) AS Minimum_Price,
    MAX(Modal_Price) AS Maximum_Price
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Grade
ORDER BY Average_Modal_Price DESC;

SELECT
    Market,
    COUNT(*) AS Above_Average_Records,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
WHERE Modal_Price > (
    SELECT AVG(Modal_Price)
    FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
)
GROUP BY Market
ORDER BY Average_Modal_Price DESC;

WITH MarketStats AS (
    SELECT
        Market,
        COUNT(*) AS Total_Records,
        AVG(Modal_Price) AS Average_Price
    FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
    GROUP BY Market
),
OverallStats AS (
    SELECT AVG(Modal_Price) AS Overall_Average
    FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
)
SELECT
    M.Market,
    M.Total_Records,
    ROUND(M.Average_Price, 2) AS Average_Price,
    ROUND(O.Overall_Average, 2) AS Overall_Average,
    CASE
        WHEN M.Average_Price > O.Overall_Average
        THEN 'Above Average'
        ELSE 'Below Average'
    END AS Market_Performance
FROM MarketStats M
CROSS JOIN OverallStats O
ORDER BY M.Average_Price DESC;

SELECT
    Market,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    RANK() OVER (
        ORDER BY AVG(Modal_Price) DESC
    ) AS Market_Rank
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Market
ORDER BY Market_Rank;

SELECT
    Market,
    Arrival_Date,
    Modal_Price,
    LAG(Modal_Price) OVER (
        PARTITION BY Market
        ORDER BY Arrival_Date
    ) AS Previous_Day_Price,
    Modal_Price - LAG(Modal_Price) OVER (
        PARTITION BY Market
        ORDER BY Arrival_Date
    ) AS Price_Change
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
ORDER BY Market, Arrival_Date;

SELECT
    Arrival_Date,
    Market,
    Modal_Price,
    CASE
        WHEN Modal_Price >= 5000 THEN 'Very High Price'
        WHEN Modal_Price >= 3000 THEN 'High Price'
        ELSE 'Normal Price'
    END AS Price_Category
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
WHERE Modal_Price >= 3000
ORDER BY Modal_Price DESC;

