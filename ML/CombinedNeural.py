from imblearn.under_sampling import NearMiss
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Activation
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


# One-hot encode the target labels
y_train_encoded = to_categorical(y_train, num_classes=3)
y_test_encoded = to_categorical(y_test, num_classes=3)

print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)


# Define the model
model = Sequential()

# Add the CNN layer
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(10, 1)))
model.add(MaxPooling1D(pool_size=2))

# Add LSTM layer
model.add(LSTM(50))

# Add output layer
model.add(Dense(3))  # Output for 3 classes
model.add(Activation('softmax'))  # Softmax for multi-class classification

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train_encoded, epochs=40, batch_size=32, validation_data=(X_test, y_test_encoded))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test_encoded)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)
#0.6724 with 20 epochs.  #0.7029 or 0.7324? with 30 epochs #0.75534 with 40 epochs #0.7214 with 50 epochs


# Save model to disk using Keras built-in method
model.save("CombinedNeural_model.h5")
#keras.saving.save_model(model, 'CombinedNeural_model.keras')