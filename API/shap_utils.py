from typing import DefaultDict
import pandas as pd
from API.constants import AttributeNames
from DataLoader_ey import data_loader
from tensorflow.keras.models import load_model
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from models import InstanceInfo
from constants import rename_dict, inv_rename

class ShapPreprocess():
    def __init__(self):
        # load dataset
        data = data_loader()
        # numerical column names
        numericals = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        # categorical column names
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

    def transform_API_response(self, instance: InstanceInfo):
        needed_attrs = [e.value for e in AttributeNames if e not in [AttributeNames.NN_confidence, AttributeNames.NN_recommendation]]
        df_dict = {}
        # use correct attribute names for model
        for name in needed_attrs:
            df_dict[inv_rename[name]] = instance.__dict__[name]
        
        # TODO continue here
        
