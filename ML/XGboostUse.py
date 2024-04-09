import numpy as np
import joblib

# Kaydedilmiş modeli yükle
loaded_model = joblib.load("xgboost_model.pkl")

# Örnek bir giriş verisi
#new_data = np.array([[5.1, 3.5, 1.4, 0.2]])
# Read X_test and y_test from the text file
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

#Model testing
predictions = loaded_model.predict(X_test)


# Tahmin sonucuna göre uygun sınıfı eşleştir
class_mapping = {0: "Non-Failure", 1: "Failure", 2: "Maintenance"}

predicted_classes = [class_mapping[prediction] for prediction in predictions]

# Gerçek sınıfları da sınıf isimlerine dönüştür
actual_classes = [class_mapping[actual] for actual in y_test]

# Tahminlerle gerçek sınıfları karşılaştır ve doğruluk hesapla
accuracy = (np.array(predicted_classes) == np.array(actual_classes)).mean()
print("Test Accuracy:", accuracy)
#print("Prediction:", predicted_classes)