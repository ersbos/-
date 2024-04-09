from imblearn.under_sampling import NearMiss
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import pathlib
import joblib
import numpy as np


DATA_PATH = pathlib.Path("C:/Users/umitc/Desktop/python_vscode/Aselsan proje/proje/data/")

df = pd.read_feather(DATA_PATH / "Classification.feather")
df["Target"].value_counts()

X = df.drop(columns=["timestamp", "Target"]) # this is purely a classification no time steps are needed
y = df["Target"]

nm_undersampler = NearMiss(version=3, n_neighbors_ver3=3, n_jobs=-1) # Warning takes very long to run
X, y = nm_undersampler.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

# Save X_test and y_test to a text file
with open("test_data.txt", "w") as file:
    # Write X_test
    file.write("X_test:\n")
    np.savetxt(file, X_test, delimiter=",")
    
    # Write y_test
    file.write("\ny_test:\n")
    np.savetxt(file, y_test, delimiter=",", fmt="%d")


