import pandas as pd
import matplotlib.pyplot as plt  # Use 'pyplot' instead of 'as plt'
import yfinance as yf

from adtk.data import validate_series
from adtk.visualization import plot
from adtk.detector import ThresholdAD, PersistAD , SeasonalAD

# Read the dataset
data = pd.read_csv("dataset_train.csv")

# Select only the required columns and convert timestamp to datetime
data = data[["timestamp", "Oil_temperature"]]
data["timestamp"] = pd.to_datetime(data["timestamp"])

# Set the timestamp column as the index
data = data.set_index("timestamp")

# Extract the oil temperature data
oil_temperature_data = data["Oil_temperature"]

# Validate the series (optional but recommended)
oil_temperature_data = validate_series(oil_temperature_data)

# Initialize the threshold anomaly detector
persist_detector = SeasonalAD()

# Detect anomalies
anomalies = persist_detector.fit_detect(oil_temperature_data)

# Plot the data and anomalies
plot(oil_temperature_data, anomaly=anomalies, anomaly_color="red", anomaly_tag="marker")
plt.show()
#https://arundo-adtk.readthedocs-hosted.com/en/stable/