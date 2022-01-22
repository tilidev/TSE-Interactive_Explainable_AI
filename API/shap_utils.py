from typing import DefaultDict
import pandas as pd
from constants import AttributeNames
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
        data = data.drop(columns="label")
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

        self.model = load_model('smote_ey.tf')

    def transform(self, df: pd.DataFrame):
        return self.pre.transform(df)

    def transform_API_response(self, instance: InstanceInfo):
        '''Returns the API response for a dataset instance (loan application) as a transformed dataFrame preprocessed for Shap'''
        needed_attrs = [e.value for e in AttributeNames if e not in [AttributeNames.NN_confidence, AttributeNames.NN_recommendation, AttributeNames.ident]]
        df_dict = {}
        # use correct attribute names for model
        for name in needed_attrs:
            df_dict[inv_rename[name]] = [instance[name]]
        df = pd.DataFrame(df_dict)
        print(df.shape)
        return self.transform(df)
        
        
