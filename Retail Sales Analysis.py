# Retail Sales Analysis in Python

# Import Libraries
import pandas as pd
import numpy as np

# -----------------------------
# Load Data
# -----------------------------
# If data is in CSV
df = pd.read_csv("Retail Sales Analysis.csv")

# For demonstration, creating empty DataFrame with same columns
columns = ['transaction_id', 'sale_date', 'sale_time', 'customer_id', 
           'gender', 'age', 'category', 'quantity', 'price_per_unit', 
           'purchase_cost', 'total_sale']
df = pd.DataFrame(columns=columns)

# -----------------------------
# Preview Data
# -----------------------------
print(df.head(10))

# -----------------------------
# Total Sales (Number of Transactions)
# -----------------------------
print("Total transactions:", len(df))

# -----------------------------
# Data Cleaning Checks
# -----------------------------
null_rows = df[df.isnull().any(axis=1)]
print("Rows with Null values:\n", null_rows)

# Delete Null Records
df = df.dropna()

# -----------------------------
# Data Exploration
# -----------------------------
# Total Unique Customers
print("Unique customers:", df['customer_id'].nunique())

# Total Unique Categories
print("Unique categories:", df['category'].nunique())
print(df['category'].value_counts())

# -----------------------------
# Q1: Sales on 2022-11-05
# -----------------------------
q1 = df[df['sale_date'] == '2022-11-05']
print(q1)

# -----------------------------
# Q2: Clothing transactions (quantity >= 5) in November 2022
# -----------------------------
df['sale_date'] = pd.to_datetime(df['sale_date'])
q2 = df[
    (df['category'] == 'Clothing') &
    (df['sale_date'].dt.to_period('M') == '2022-11') &
    (df['quantity'] >= 4)
]
print(q2)

# -----------------------------
# Q3: Total sales in each category
# -----------------------------
q3 = df.groupby('category').agg(
    net_sale=('total_sale', 'sum'),
    total_orders=('category', 'count')
).reset_index()
print(q3)

# -----------------------------
# Q4: Average age of buyers in Beauty
# -----------------------------
q4 = round(df[df['category'] == 'Beauty']['age'].mean(), 2)
print("Average age (Beauty):", q4)

# -----------------------------
# Q5: Transactions where total_sale > 1000
# -----------------------------
q5 = df[df['total_sale'] > 1000]
print(q5)

# -----------------------------
# Q6: Total transactions by gender in each category
# -----------------------------
q6 = df.groupby(['category', 'gender']).size().reset_index(name='total_trans')
q6 = q6.sort_values(['category', 'gender'])
print(q6)

# -----------------------------
# Q7: Average sale per month & best month each year
# -----------------------------
df['year'] = df['sale_date'].dt.year
df['month'] = df['sale_date'].dt.month
monthly_avg = df.groupby(['year','month'])['total_sale'].mean().reset_index()
monthly_avg['rank'] = monthly_avg.groupby('year')['total_sale'].rank(ascending=False, method='dense')
q7 = monthly_avg[monthly_avg['rank']==1].sort_values('year')
print(q7[['year','month','total_sale']])

# -----------------------------
# Q8: Top 5 customers by total sales
# -----------------------------
q8 = df.groupby('customer_id')['total_sale'].sum().reset_index()
q8 = q8.sort_values('total_sale', ascending=False).head(5)
print(q8)

# -----------------------------
# Q9: Number of unique customers per category
# -----------------------------
q9 = df.groupby('category')['customer_id'].nunique().reset_index(name='unique_customers')
print(q9)

# -----------------------------
# Q10: Orders by shift
# -----------------------------
df['sale_time'] = pd.to_datetime(df['sale_time'], format='%H:%M:%S').dt.time

def assign_shift(time):
    if time.hour < 12:
        return 'Morning'
    elif 12 <= time.hour <= 17:
        return 'Afternoon'
    else:
        return 'Evening'

df['shift'] = df['sale_time'].apply(assign_shift)
q10 = df.groupby('shift').size().reset_index(name='total_orders')
print(q10)

# -----------------------------
# End of Project
# -----------------------------

