from typing import DefaultDict
import pandas as pd
from pkg_resources import register_namespace_handler
from constants import AttributeNames
from DataLoader_ey import data_loader
from tensorflow.keras.models import load_model
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from models import InstanceInfo
from constants import inv_rename, rename_dict
import shap

class ShapHelperV2:
    def __init__(self, model, data: pd.DataFrame):
        """TODO"""
        self.model = model
        self.data = data
        pass

    def data_preprocess(self):
        """TODO"""
        self.data.rename(columns=rename_dict, inplace=True)
        X = self.data.drop(columns='label') # feature matrix
        y = self.data['label'] # target array
        # Create train and test split
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        self.train_data = X_train.join(pd.DataFrame(y_train, columns=['label']))
        self.test_data = X_test.join(pd.DataFrame(y_test, columns=['label']))
        self.X_train = self.train_data.drop(columns='label')
        self.X_test = self.test_data.drop(columns='label')

    def predict_proba(self, data: pd.DataFrame):
        """TODO mainly taken from explanation_utils_ey"""
        num_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        preprocessor = ColumnTransformer(
            transformers=[('num', MinMaxScaler(), num_cols),
                          ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)]
        )
        preprocessor        


class ShapHelper:
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

        model = load_model('smote_ey.tf')
        def predict_fn_shap(X):
            # Single data point has dimensions (18,) but (1, 18) is needed for preprocessing
            # Therefore, reshape input to (-1, 18)
            X_df = pd.DataFrame(X.reshape((-1,18)), columns=[e.value for e in AttributeNames if e not in [AttributeNames.NN_confidence, AttributeNames.NN_recommendation, AttributeNames.ident]])
            # Preprocess input and create nd-array
            X_transformed = preprocessor_shap.transform(X_df).toarray()
            # model.predict output has shape (n, 1) but (n,) is needed
            prob = model.predict(X_transformed).reshape(-1,)
            return prob
        self.explainer = shap.KernelExplainer(predict_fn_shap, preprocessor_shap.transform(data))

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
        return self.transform(df)
        
        
