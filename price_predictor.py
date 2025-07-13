import pandas as pd
import joblib
from datetime import datetime

raw_df = pd.read_csv("Updated_Grocery_Inventory_with_Images_Dates_seven.csv")

print(f"Initial dataset shape: {raw_df.shape}")

raw_df["Expiration_Date"] = pd.to_datetime(raw_df["Expiration_Date"], errors='coerce')
raw_df["today"] = pd.to_datetime(datetime.now().date())
raw_df["Days_to_Expiry"] = (raw_df["Expiration_Date"] - raw_df["today"]).dt.days

required_columns = ["Unit_Price", "Days_to_Expiry", "Stock_Quantity", "Inventory_Turnover_Rate"]
model_input = raw_df[required_columns].copy()

print(f"Model input shape: {model_input.shape}")

print("Cleaning Unit_Price column...")
model_input['Unit_Price'] = model_input['Unit_Price'].str.replace('$', '', regex=False).str.strip().astype(float)

for col in ['Days_to_Expiry', 'Stock_Quantity', 'Inventory_Turnover_Rate']:
    model_input[col] = pd.to_numeric(model_input[col], errors='coerce')

print(f"Shape before cleaning: {model_input.shape}")
model_input_clean = model_input.dropna()
print(f"Shape after cleaning: {model_input_clean.shape}")

if len(model_input_clean) == 0:
    print("No data remaining after cleaning!")
    exit(1)

scaler = joblib.load("feature_scaler.pkl")
model = joblib.load("xgboost_discount_model.pkl")

X_scaled = scaler.transform(model_input_clean)
predicted_prices = model.predict(X_scaled)

predicted_df = raw_df.loc[model_input_clean.index].copy()
predicted_df["Predicted_Discounted_Price"] = predicted_prices.round(2)

predicted_df.to_csv("final_output_with_predictions.csv", index=False)
print(f"Predictions saved to final_output_with_predictions.csv")
print(f"Total predictions: {len(predicted_df)}")

print("\nSample predictions:")
print(predicted_df[["Product_Name", "Unit_Price", "Predicted_Discounted_Price"]].head())