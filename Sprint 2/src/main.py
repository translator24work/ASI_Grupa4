from src.data_loading import load_data
from src.data_preprocessing import preprocess_data, encode_categorical_data, prepare_data
from src.model_training import train_model
from src.model_evaluation import evaluate_model
import joblib

# Wczytanie danych
data = load_data("data/cwurData.csv")

# Przetwarzanie i oczyszczanie danych
data_cleaned = preprocess_data(data)

# Podział na zbiory treningowy, walidacyjny i testowy
X, y = prepare_data(data_cleaned)

# Trenowanie modelu
model = train_model(X["X_train_final"], y["y_train"])

# Ewaluacja modelu na danych walidacyjnych
mse_val = evaluate_model(model, X["X_val_final"], y["y_val"])
print("Mean Squared Error on Validation Data:", mse_val)

# Zapisanie modelu
joblib.dump(model, "models/random_forest_model.pkl")
print("Model saved as 'random_forest_model.pkl'")