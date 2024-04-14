import numpy as np
from tensorflow.keras.models import load_model

# Load the saved model
loaded_model = load_model("CombinedNeural_model.h5")

with open("test_data.txt", "r") as file:
    lines = file.readlines()

# Find the index where X_test ends and y_test begins
x_test_end_index = lines.index("y_test:\n")

# Parse X_test
X_test = np.genfromtxt(lines[1:x_test_end_index], delimiter=",")

# Parse y_test
y_test = np.genfromtxt(lines[x_test_end_index + 1:], delimiter=",", dtype=int)

# Print the shapes of X_test and y_test to verify
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)

# If you need to reshape the data to match the input shape of your model (10, 1)
# you can do it as follows:

predictions = loaded_model.predict(X_test)

class_mapping = {0: "Non-Failure", 1: "Failure", 2: "Maintenance"}

predicted_classes = [class_mapping[prediction.argmax()] for prediction in predictions]

# Gerçek sınıfları da sınıf isimlerine dönüştür
actual_classes = [class_mapping[actual] for actual in y_test]

# Tahminlerle gerçek sınıfları karşılaştır ve doğruluk hesapla
accuracy = (np.array(predicted_classes) == np.array(actual_classes)).mean()
print("Test Accuracy:", accuracy)
