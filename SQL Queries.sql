-- Retail Sales Analysis Project
-- Commencing of the project

-- Create Database

CREATE DATABASE IF NOT EXISTS Retail_Sales_Analysis;
USE Retail_Sales_Analysis;
-- Create TABLE
DROP TABLE IF EXISTS retail_sales;
CREATE TABLE retail_sales (
    transaction_id INT PRIMARY KEY,	
    sale_date DATE,	 
    sale_time TIME,	
    customer_id	INT,
    gender	VARCHAR(10),
    age	INT,
    category VARCHAR(25),	
    quantity INT,
    price_per_unit DECIMAL(10,2),
    purchase_cost DECIMAL(10,2),
    total_sale DECIMAL(10,2)

);

-- Preview Data
SELECT * FROM retail_sales LIMIT 10;

-- Total Sales
SELECT COUNT(*) FROM retail_sales;

-- Data Cleaning Checks
SELECT * FROM retail_sales
WHERE 
    transaction_id IS NULL OR
    sale_date IS NULL OR 
    sale_time IS NULL OR
    gender IS NULL OR
    category IS NULL OR
    quantity IS NULL OR
    purchase_cost IS NULL OR
    total_sale IS NULL;

-- Delete Null Records
DELETE FROM retail_sales
WHERE 
    transaction_id IS NULL OR
    sale_date IS NULL OR 
    sale_time IS NULL OR
    gender IS NULL OR
    category IS NULL OR
    quantity IS NULL OR
    purchase_cost IS NULL OR
    total_sale IS NULL;
    
SET SQL_SAFE_UPDATES=1;

-- Data Exploration
-- Total Sales
SELECT COUNT(*) AS total_sale FROM retail_sales;
-- Total Unique Customers
SELECT COUNT(DISTINCT customer_id) AS unique_customers FROM retail_sales;
-- Total Unique Categories
SELECT DISTINCT category, COUNT(DISTINCT category) FROM retail_sales GROUP BY category;

-- Q1: Sales on 2022-11-05
SELECT * FROM retail_sales
WHERE sale_date = '2022-11-05';

-- Q2: All transactions with category='Clothing' and quantity >= 5 in November 2022
SELECT * FROM retail_sales
WHERE category = 'Clothing' AND
      sale_date BETWEEN '2022-11-01' AND '2022-11-30' 
    AND quantity >= 5;
    
-- Q3: Total sales in each category
SELECT 
    category,
    SUM(total_sale) AS net_sale,
    COUNT(category) AS total_orders
FROM retail_sales
GROUP BY category;

-- Q4: Average age of buyers in the category of Beauty
SELECT ROUND(AVG(age), 2) AS avg_age
FROM retail_sales
WHERE category = 'Beauty';

-- Q5: Transactions where total_sale is greater than 1000
SELECT * FROM retail_sales
WHERE total_sale > 1000;

-- Q6: Total transactions made by each gender in each category
SELECT 
    category,
    gender,
    COUNT(*) AS total_trans
FROM retail_sales
GROUP BY category, gender
ORDER BY category, gender;

-- Q7: Average sale for each month and the best selling month in each year
SELECT 
    year,
    month,
    avg_sale
FROM (
    SELECT 
        YEAR(sale_date) AS year,
        MONTH(sale_date) AS month,
        AVG(total_sale) AS avg_sale,
        RANK() OVER (PARTITION BY YEAR(sale_date) ORDER BY AVG(total_sale) DESC) AS rnk
    FROM retail_sales
    GROUP BY YEAR(sale_date), MONTH(sale_date)
) AS ranked_sales
WHERE rnk = 1
ORDER BY year;

-- Q8: Top 5 customers based on the highest total sales
SELECT 
    customer_id,
    SUM(total_sale) AS total_sales
FROM retail_sales
GROUP BY customer_id
ORDER BY total_sales DESC
LIMIT 5;

-- Q9: Number of Unique customers who purchased from each category
SELECT 
    category,    
    COUNT(DISTINCT customer_id) AS unique_customers
FROM retail_sales
GROUP BY category;

-- Q10: Orders by shift (Create each shift and number of orders for example Morning<-12, Afternoon between 12 & 17 etc.) 
SELECT 
    CASE
        WHEN HOUR(sale_time) < 12 THEN 'Morning'
        WHEN HOUR(sale_time) BETWEEN 12 AND 17 THEN 'Afternoon'
        ELSE 'Evening'
    END AS shift,
    COUNT(sale_time) AS total_orders
FROM retail_sales
GROUP BY shift;

-- End of project
