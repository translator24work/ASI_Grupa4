import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

def preprocess_data(df):
    # Usunięcie rekordów zawierających brakujące wartości w kolumnie 'broad_impact'
    df = df.dropna(subset=['broad_impact'])

    # Normalizacja danych numerycznych (np. numerycznych kolumn od 0 do 10)
    numerical_cols = df.columns[0:11]  # Załóżmy, że kolumny od 0 do 10 są numeryczne
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    # Inne operacje przetwarzania danych można dodać tutaj
    # ...

    return df

def encode_categorical_data(X_train, X_val, X_test, categorical_cols):
    # Inicjalizacja obiektu kodowania gorących jednostek
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')

    # Dopasowanie i przekształcenie danych tekstowych za pomocą kodowania gorących jednostek
    X_train_encoded = encoder.fit_transform(X_train[categorical_cols])
    X_val_encoded = encoder.transform(X_val[categorical_cols])
    X_test_encoded = encoder.transform(X_test[categorical_cols])

    X_train_numeric = X_train.drop(categorical_cols, axis=1)
    X_val_numeric = X_val.drop(categorical_cols, axis=1)
    X_test_numeric = X_test.drop(categorical_cols, axis=1)

    # Połączenie przekształconych danych z kodowaniem gorących jednostek z danymi numerycznymi
    X_train_final = np.hstack((X_train_encoded, X_train_numeric))
    X_val_final = np.hstack((X_val_encoded, X_val_numeric))
    X_test_final = np.hstack((X_test_encoded, X_test_numeric))

    return X_train_final, X_val_final, X_test_final


def prepare_data(X_train_numeric, X_val_numeric, X_test_numeric, X_train_final, X_val_final, X_test_final, y_train, y_val, y_test):
    # Przygotowanie danych do modelu
    X_train = np.hstack((X_train_numeric, X_train_final))
    X_val = np.hstack((X_val_numeric, X_val_final))
    X_test = np.hstack((X_test_numeric, X_test_final))

    return X_train, X_val, X_test, y_train, y_val, y_test