from imblearn.under_sampling import NearMiss
from sklearn.preprocessing import StandardScaler
from pyod.models.xgbod import XGBOD
import pandas as pd
import pathlib
import numpy as np

# Load data
DATA_PATH = pathlib.Path("C:/Users/umitc/Desktop/python_vscode/Aselsan proje/proje/data/")
df = pd.read_feather(DATA_PATH / "Classification.feather")

# Extract features and target variable
X = df.drop(columns=["timestamp", "Target"])
y = df["Target"]

# Apply NearMiss for undersampling (if needed)
nm_undersampler = NearMiss(version=3, n_neighbors_ver3=3, n_jobs=-1)
X_resampled, y_resampled = nm_undersampler.fit_resample(X, y)

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_resampled)

# Initialize and fit the XGBOD model
model = XGBOD()
model.fit(X_scaled, np.zeros(X_scaled.shape[0]))

# Predict outliers
outliers = model.predict(X_scaled)

# Print the indices of outliers
print("Indices of outliers:", outliers)
