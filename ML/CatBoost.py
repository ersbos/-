from imblearn.under_sampling import NearMiss
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from catboost import CatBoostClassifier, Pool
from sklearn.metrics import accuracy_score
import pandas as pd
import pathlib
import joblib

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


# Define the CatBoost model
model = CatBoostClassifier(iterations=100, depth=2, learning_rate=0.1, loss_function='MultiClass')

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
#0.636704

# Save model to disc
joblib.dump(model, "Catboost_model.pkl")