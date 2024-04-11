from imblearn.under_sampling import NearMiss
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Flatten
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


# Define the model
model = Sequential()

# Add the CNN layer
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(10, 1)))
model.add(MaxPooling1D(pool_size=2))

# Add LSTM layer
model.add(LSTM(50))

# Add output layer
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)
#0.46


# Save model to disc
joblib.dump(model, "CombinedNeural_model.pkl")