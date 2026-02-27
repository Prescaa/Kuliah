import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class Evaluator:
    @staticmethod
    def calculate_mape(y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        mask = y_true != 0
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

    @classmethod
    def get_all_metrics(cls, y_true, y_pred):
        return {
            "MAE": mean_absolute_error(y_true, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
            "MAPE": cls.calculate_mape(y_true, y_pred),
            "R2": r2_score(y_true, y_pred)
        }