import pandas as pd
from DataLoader_ey import data_loader
from tensorflow.keras.models import load_model
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

class ShapPreprocess():
    def __init__(self):
        # load dataset
        data = data_loader()
        # load model
        model = load_model('smote_ey.tf')

        numericals = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categoricals = data.select_dtypes(include=['object', 'category']).columns.tolist()

        preprocessor_shap = ColumnTransformer(
            transformers=[
                ('num', MinMaxScaler(), numericals),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categoricals)
            ]
        )
        preprocessor_shap.fit(data)

        self.pre = preprocessor_shap
    
    def transform(self, df: pd.DataFrame):
        return self.pre.transform(df)