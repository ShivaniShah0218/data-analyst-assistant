import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Create sample data
n_rows = 100
data = {
    "ID": range(1, n_rows + 1),
    "Age": np.random.normal(loc=35, scale=10, size=n_rows).astype(int),  # Normally distributed ages
    "Salary": np.random.normal(loc=50000, scale=15000, size=n_rows),     # Normally distributed salaries
    "Department": np.random.choice(["Sales", "HR", "Engineering", "Marketing"], size=n_rows),
    "JoinDate": pd.date_range(start="2015-01-01", periods=n_rows, freq='M')
}

df = pd.DataFrame(data)

# Introduce null values
df.loc[np.random.choice(df.index, size=5, replace=False), "Age"] = np.nan
df.loc[np.random.choice(df.index, size=5, replace=False), "Salary"] = np.nan
df.loc[np.random.choice(df.index, size=5, replace=False), "Department"] = np.nan

# Introduce outliers
df.loc[np.random.choice(df.index, size=2), "Age"] = [5, 99]               # Unrealistic ages
df.loc[np.random.choice(df.index, size=2), "Salary"] = [1000000, -5000]  # Extreme salary values

# Introduce anomalous data
df.loc[10, "JoinDate"] = "Not a date"
df.loc[20, "Salary"] = "Unknown"

# Save to CSV
df.to_csv("sample_test_data.csv", index=False)
print("CSV file 'sample_test_data.csv' created.")
