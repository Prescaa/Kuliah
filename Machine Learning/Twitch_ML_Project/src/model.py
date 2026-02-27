from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

class ModelFactory:
    @staticmethod
    def get_baseline():
        return LinearRegression()

    @staticmethod
    def get_ridge(alpha=1.0):
        return Ridge(alpha=alpha)

    @staticmethod
    def get_lasso(alpha=0.01):
        return Lasso(alpha=alpha)

    @staticmethod
    def get_poly_ridge(degree=2, alpha=1.0):
        return Pipeline([
            ("poly", PolynomialFeatures(degree=degree, interaction_only=True)),
            ("ridge", Ridge(alpha=alpha))
        ])