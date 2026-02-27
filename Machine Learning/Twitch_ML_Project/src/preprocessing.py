import pandas as pd
import numpy as np

class Preprocessor:
    def __init__(self):
        self.game_freq = {}

    def clean_data(self, df):
        df = df.dropna(subset=['Game']).copy()
        return df

    def feature_engineering(self, df):
        df['efficiency_ratio'] = df['Hours_watched'] / (df['Hours_streamed'] + 1)
        df['viewer_per_channel'] = df['Avg_viewers'] / (df['Avg_channels'] + 1)
        
        self.game_freq = df['Game'].value_counts().to_dict()
        df['game_popularity_enc'] = df['Game'].map(self.game_freq)
        
        df['month_sin'] = np.sin(2 * np.pi * df['Month'].astype(int)/12)
        df['month_cos'] = np.cos(2 * np.pi * df['Month'].astype(int)/12)
        
        df['era_enc'] = pd.cut(df['Year'], bins=[2015, 2018, 2021, 2025], labels=[0, 1, 2]).astype(int)
        return df

    def remove_outliers(self, df, column):
        y_log = np.log1p(df[column])
        q1, q3 = y_log.quantile(0.25), y_log.quantile(0.75)
        iqr = q3 - q1
        mask = (y_log >= (q1 - 2.5 * iqr)) & (y_log <= (q3 + 2.5 * iqr))
        return df[mask].copy()

    def transform_target(self, y):
        return np.log1p(y)

    def inverse_target(self, y_log):
        return np.expm1(y_log)