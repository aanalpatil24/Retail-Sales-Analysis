# Retail Sales Analysis Project 

# Commencement of the Project 

# Import Libraries 
import pandas as pd 
import numpy as np

# Step 1 - Load Data
df = pd.read_csv("retail_sales.csv", encoding_errors='ignore')


# Step 2 - Data Cleaning

# Remove duplicates
df.drop_duplicates(inplace=True)

# Drop rows with any critical nulls
critical_cols = ['transaction_id','sale_date','sale_time','gender','category','quantity','purchase_cost','total_sale']
df.dropna(subset=critical_cols, inplace=True)

# Convert date and time columns
df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
df['sale_time'] = pd.to_datetime(df['sale_time'], format='%H:%M:%S', errors='coerce').dt.time


# Step 3 - Data Exploration
print("Total transactions:", len(df))
print("Unique customers:", df['customer_id'].nunique())
print("Unique categories:", df['category'].nunique())
print(df['category'].value_counts())


# Q1: Sales on 2022-11-05
q1 = df[df['sale_date'] == '2022-11-05']
print(q1)


# Q2: Clothing transactions (quantity >= 5) in November 2022
q2 = df[
    (df['category'] == 'Clothing') &
    (df['sale_date'].dt.to_period('M') == '2022-11') &
    (df['quantity'] >= 5)
]
print(q2)


# Q3: Total sales in each category
q3 = df.groupby('category').agg(
    net_sale=('total_sale', 'sum'),
    total_orders=('category', 'count')
).reset_index()
print(q3)


# Q4: Average age of buyers in Beauty
q4 = round(df[df['category']=='Beauty']['age'].mean(), 2)
print("Average age (Beauty):", q4)


# Q5: Transactions where total_sale > 1000
q5 = df[df['total_sale'] > 1000]
print(q5)


# Q6: Total transactions by gender in each category
q6 = df.groupby(['category','gender']).size().reset_index(name='total_trans').sort_values(['category','gender'])
print(q6)


# Q7: Best selling month in each year
df['year'] = df['sale_date'].dt.year
df['month'] = df['sale_date'].dt.month
monthly_sales = df.groupby(['year','month'])['total_sale'].sum().reset_index()
monthly_sales['rank'] = monthly_sales.groupby('year')['total_sale'].rank(method='dense', ascending=False)
q7 = monthly_sales[monthly_sales['rank']==1].sort_values('year')
print(q7[['year','month','total_sale']])


# Q8: Top 5 customers by total sales
q8 = df.groupby('customer_id')['total_sale'].sum().reset_index(name='total_sales') \
        .sort_values('total_sales', ascending=False).head(5)
print(q8)


# Q9: Number of unique customers per category
q9 = df.groupby('category')['customer_id'].nunique().reset_index(name='unique_customers')
print(q9)


# Q10: Orders by shift
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

# End of Retail Sales Project

