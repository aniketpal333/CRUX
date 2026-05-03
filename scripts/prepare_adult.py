"""Add the canonical column header to UCI Adult and clean basic issues."""
import pandas as pd

COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country",
    "income",
]

df = pd.read_csv("data/adult.data", names=COLUMNS, skipinitialspace=True, na_values="?")
df.to_csv("data/adult.csv", index=False)
print(f"Shape: {df.shape}")
print(df["income"].value_counts())