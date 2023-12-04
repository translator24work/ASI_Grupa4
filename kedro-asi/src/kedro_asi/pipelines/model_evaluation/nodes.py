from sklearn.metrics import mean_squared_error

def evaluate_model(model, X_val, y_val):
    predictions_val = model.predict(X_val)
    mse_val = mean_squared_error(y_val, predictions_val)
    return mse_val