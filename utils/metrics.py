import numpy as np

def MSE(y_true, y_pred):
    return np.mean((np.array(y_true)-np.array(y_pred))**2)

def MAE(y_true, y_pred):
    return np.mean(np.abs(np.array(y_true)-np.array(y_pred)))