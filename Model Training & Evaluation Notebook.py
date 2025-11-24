import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import xgboost as xgb

# ===============================
# SETTINGS
# ===============================
filename = "extended_fmcg_demand_forecasting_cleaned.csv"

# ===============================
# CHECK WORKING DIRECTORY
# ===============================
print("Current working directory:", os.getcwd())

# ===============================
# TRY TO LOAD CSV
# ===============================
if not os.path.exists(filename):
    print(f"ERROR: File '{filename}' was not found in the directory shown above.")
    print("Please copy the CSV file into this folder or provide the full path.")
    exit()

print(f"File '{filename}' found. Loading dataset...")

df = pd.read_csv(filename)
print("Dataset loaded successfully.")
print(df.head())

# ===============================
# TRAIN TEST SPLIT
# Adjust these column names to match your dataset
# ===============================
# Example feature and target columns
X = df.drop("target", axis=1)   # Change "target" to your actual label column
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Data split into training and testing sets.")

# ===============================
# MODEL 1: Linear Regression
# ===============================
print("\nTraining Linear Regression...")
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

print("Linear Regression Results:")
print("MAE:", mean_absolute_error(y_test, lr_pred))
print("MSE:", mean_squared_error(y_test, lr_pred))
print("R2:", r2_score(y_test, lr_pred))

# ===============================
# MODEL 2: XGBoost
# ===============================
print("\nTraining XGBoost...")
xgb_model = xgb.XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)

print("XGBoost Results:")
print("MAE:", mean_absolute_error(y_test, xgb_pred))
print("MSE:", mean_squared_error(y_test, xgb_pred))
print("R2:", r2_score(y_test, xgb_pred))


