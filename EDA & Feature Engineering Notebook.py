# -----------------------------------------------------
# FMCG Demand Forecasting - EDA & Feature Engineering
# -----------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings

warnings.filterwarnings('ignore')

# Set plotting styles
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# -----------------------------------------------------
# 1. Load Dataset with Full File Path
# -----------------------------------------------------
file_path = r"C:\Users\favour.chigozie\Downloads\extended_fmcg_demand_forecasting_cleaned.csv"

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError("File not found at: " + file_path)

df = pd.read_csv(file_path)
print("File loaded successfully!")
print("Dataset Shape:", df.shape)

# -----------------------------------------------------
# 2. Inspect Data
# -----------------------------------------------------
print("\nDataset Overview:")
print("Columns:", df.columns.tolist())
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())

# -----------------------------------------------------
# 3. Convert Date Column
# -----------------------------------------------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
print("\nDate column converted successfully!")
print("Date Range:", df['Date'].min(), "to", df['Date'].max())

# -----------------------------------------------------
# 4. Basic Statistics
# -----------------------------------------------------
print("\nBasic Statistics:")
print(df[['Sales_Volume', 'Price', 'Supplier_Cost', 'Stock_Level']].describe())

# -----------------------------------------------------
# 5. Feature Engineering
# -----------------------------------------------------
print("\nPerforming Feature Engineering...")

# Date-based features
df['Month'] = df['Date'].dt.month
df['Quarter'] = df['Date'].dt.quarter
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['WeekOfYear'] = df['Date'].dt.isocalendar().week
df['Is_Weekend'] = (df['DayOfWeek'] >= 5).astype(int)
df['Year'] = df['Date'].dt.year

# Profit-related features
df['Profit_Margin'] = df['Price'] - df['Supplier_Cost']
df['Margin_Percentage'] = (df['Profit_Margin'] / df['Price']) * 100

# Stock-out flag
df['Stock_Out_Risk'] = (df['Stock_Level'] < df['Sales_Volume']).astype(int)

# Competitor price proxy
df['Avg_Category_Price'] = df.groupby(
    ['Product_Category', 'Store_Location', 'Date']
)['Price'].transform('mean')

df['Price_Ratio_To_Avg'] = df['Price'] / df['Avg_Category_Price']

print("Feature engineering completed.")
print("New Dataset Shape:", df.shape)
print("New Columns:", df.columns.tolist())

# -----------------------------------------------------
# 6. Exploratory Data Analysis (EDA)
# -----------------------------------------------------
print("\nStarting Exploratory Data Analysis...")

plt.figure(figsize=(15, 12))

# 1. Average Sales by Category
plt.subplot(2, 3, 1)
category_sales = df.groupby('Product_Category')['Sales_Volume'].mean().sort_values(ascending=False)
sns.barplot(x=category_sales.values, y=category_sales.index)
plt.title('Average Sales Volume by Product Category')
plt.xlabel('Average Sales Volume')

# 2. Price vs Sales Volume (colored by promotion)
plt.subplot(2, 3, 2)
sample_df = df.sample(1000, random_state=42)
sns.scatterplot(data=sample_df, x='Price', y='Sales_Volume', hue='Promotion', alpha=0.6)
plt.title('Price vs Sales Volume (Promotion Highlight)')

# 3. Sales by Store Location & Promotion
plt.subplot(2, 3, 3)
location_promo_sales = df.groupby(['Store_Location', 'Promotion'])['Sales_Volume'].mean().reset_index()
sns.barplot(data=location_promo_sales, x='Store_Location', y='Sales_Volume', hue='Promotion')
plt.title('Sales by Location and Promotion')

# 4. Monthly Trend
plt.subplot(2, 3, 4)
monthly_sales = df.groupby(['Year', 'Month'])['Sales_Volume'].mean().reset_index()
monthly_sales['Year_Month'] = monthly_sales['Year'].astype(str) + '-' + monthly_sales['Month'].astype(str)
plt.plot(monthly_sales['Year_Month'], monthly_sales['Sales_Volume'], marker='o')
plt.title('Monthly Sales Trend')
plt.xticks(rotation=45)

# 5. Price Distribution by Category
plt.subplot(2, 3, 5)
sns.boxplot(data=df, x='Product_Category', y='Price')
plt.title('Price Distribution by Category')
plt.xticks(rotation=45)

# 6. Stock Level vs Sales
plt.subplot(2, 3, 6)
sns.scatterplot(data=sample_df, x='Stock_Level', y='Sales_Volume', alpha=0.6)
plt.title('Stock Level vs Sales Volume')

plt.tight_layout()
plt.savefig('eda_insights.png', dpi=300, bbox_inches='tight')
plt.show()

# -----------------------------------------------------
# 7. Correlation Heatmap
# -----------------------------------------------------
numeric_cols = [
    'Sales_Volume', 'Price', 'Promotion', 'Supplier_Cost', 
    'Stock_Level', 'Profit_Margin', 'Price_Ratio_To_Avg'
]

correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, square=True, fmt='.2f')
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# -----------------------------------------------------
# 8. Key Insights
# -----------------------------------------------------
print("\n=================================================")
print("KEY EDA INSIGHTS")
print("=================================================")

# Price correlation with sales
corr_price_sales = df['Price'].corr(df['Sales_Volume'])
print("1. Price–Sales Correlation:", round(corr_price_sales, 3))

# Promotion effectiveness
promo_effectiveness = df.groupby('Store_Location').apply(
    lambda x: x[x['Promotion'] == 1]['Sales_Volume'].mean() /
              x[x['Promotion'] == 0]['Sales_Volume'].mean() - 1
).sort_values(ascending=False)

print("\n2. Promotion Effectiveness by Location (% Increase):")
for location, effect in promo_effectiveness.items():
    print(" ", location, ":", format(effect, ".2%"))

# Category price ranges
print("\n3. Price Ranges by Category:")
for category in df['Product_Category'].unique():
    cat_data = df[df['Product_Category'] == category]
    min_p = cat_data['Price'].min()
    max_p = cat_data['Price'].max()
    avg_p = cat_data['Price'].mean()
    print(f" {category}: ${min_p:.2f} - ${max_p:.2f} (Avg: ${avg_p:.2f})")

# -----------------------------------------------------
# 9. Save Engineered Dataset
# -----------------------------------------------------
output_path = r"C:\Users\favour.chigozie\Downloads\bosch_pricing_engineered.csv"
df.to_csv(output_path, index=False)

print("\nEngineered dataset saved to:")
print(output_path)
print("Final dataset shape:", df.shape)

# -----------------------------------------------------
# 10. Seasonal Sales Trend
# -----------------------------------------------------
print("\n=================================================")
print("SEASONAL ANALYSIS")
print("=================================================")

monthly_category = df.groupby(['Product_Category', 'Month'])['Sales_Volume'].mean().reset_index()

plt.figure(figsize=(12, 8))
for category in df['Product_Category'].unique():
    category_data = monthly_category[monthly_category['Product_Category'] == category]
    plt.plot(category_data['Month'], category_data['Sales_Volume'], 
             marker='o', label=category, linewidth=2)

plt.title('Monthly Sales Patterns by Product Category')
plt.xlabel('Month')
plt.ylabel('Average Sales Volume')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('seasonal_patterns.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nEDA completed successfully!")
