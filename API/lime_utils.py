from operator import index
import pandas as pd
import numpy as np
import tensorflow as tf
import lime
import lime.lime_tabular
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from DataLoader_ey import data_loader 
from DataLoader_ey import preprocessX 
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from constants import rename_dict
import json

class LimeHelper():
    def __init__(self):
        # Read credit data
        data = data_loader()
        self.data = data
        # Load tensorflow model
        self.model = load_model('smote_ey.tf')
        #steps from data_preprocess
        data.rename(columns=rename_dict, inplace=True)
        X_train = data.drop(columns='label')
        X = X_train.copy()
        #steps from exp_preprocess
        feature_names = X_train.columns.to_list()
        cat_cols = X_train.select_dtypes(include=['object', 'category']).columns.to_list()
        num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.to_list()
        cat_indices = [feature_names.index(col) for col in cat_cols]
        cat_names = {}
        for cat_idx in cat_indices:
            # Fit label encoder on training data and transform respective column in training and test data
            le = LabelEncoder()
            le.fit(X_train.iloc[:, cat_idx])
            X_train.iloc[:, cat_idx] = le.transform(X_train.iloc[:, cat_idx])
            # Extend dictionary with array of categories and index as key
            cat_names[cat_idx] = le.classes_
            
        preprocessor_le = ColumnTransformer(
                transformers=[('num', MinMaxScaler(), num_cols),
                            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)])
        preprocessor_le.fit(X_train)
        self.prep = preprocessor_le
        self.X_train = X_train
        self.cat_names = cat_names
        self.X = X
        self.explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values, feature_names=feature_names,
                                                    class_names=['Approved', 'Rejected'],
                                                    discretize_continuous=True, mode='classification',
                                                    categorical_features=cat_indices, categorical_names=cat_names,
                                                    feature_selection='lasso_path' )


    def predict_fn(self,X):
        # Single data point has dimensions (18,) but (1, 18) is needed for preprocessing
        # Therefore, reshape input to (-1, 18)
        X_df = pd.DataFrame(X.reshape((-1, 18)), columns=self.X_train.columns)
        # Preprocess input and create nd-array
        X_transformed = self.prep.transform(X_df).toarray()
        # model.predict output has shape (n, 1) but (n,) is needed
        prob = self.model.predict(X_transformed).reshape(-1, )
        # Return predictions in correct format, dim = (n, 2), note that the first entry
        # has to represent P(y=0 | X)
        proba_predictions = np.array([1 - prob, prob]).transpose()
        return proba_predictions

    def preprocess_new_data(self,X_df):
            """
            Function to preprocess new data for LIME and anchor explanations
            :param X_df:
            :return:
            """
            data = X_df.copy()
            # List of feature names
            feature_names = self.X.columns.to_list()

            # Lists of categorical and numerical feature names (needed for preprocessing)
            cat_cols = self.X.select_dtypes(include=['object', 'category']).columns.to_list()

            # List of indices of categorical features
            cat_indices = [feature_names.index(col) for col in cat_cols]

            # Label encoding
            
            for cat_idx in cat_indices:
                # Fit label encoder on training data and transform respective column
                le = LabelEncoder()
                le.fit(self.X.iloc[:, cat_idx])
                data.iloc[:, cat_idx] = le.transform(data.iloc[:, cat_idx])
            return data

    def get_lime_exp(self, explainer, prediction_function, idx, data_source, **kwargs):
        data_le = self.preprocess_new_data(data_source)
        print(type(data_le))
        print(data_le)
        #print(type(data_le[0]))
        lime_exp = explainer.explain_instance(data_le.values[idx], prediction_function, **kwargs)
        return lime_exp

    
l = LimeHelper()
l.__init__()

desc = {
  "id": 100,
  "balance": "no account",
  "duration": 6,
  "history": "delay payment of previous loans",
  "purpose": "furniture",
  "amount": 1000,
  "savings": "no savings account at this bank",
  "employment": "unemployed",
  "available_income": "less than 20%",
  "residence": "more than 7 years",
  "assets": "none",
  "age": 21,
  "other_loans": "no additional loans",
  "housing": "rent",
  "previous_loans": "1",
  "job": "unskilled (non-resident)",
  "other_debtors": "none",
  "people_liable": "0 to 2",
  "telephone": "yes",
  "NN_recommendation": "Approve",
  "NN_confidence": 0.9
}
d = json.dumps(desc)
d1 = json.loads(d)
k = pd.DataFrame(d1, index = [0])
print(l.X.iloc[6])
element = l.data.drop(columns='label')
k.drop(columns=['id','NN_recommendation','NN_confidence'], inplace=True)
exp = l.get_lime_exp(l.explainer, l.predict_fn, 0,k, num_features=6)
print(k)
#data = l.prep.transform(k)
'''
element = l.data.drop(columns='label')
exp = l.get_lime_exp(l.explainer, l.predict_fn, 0,element, num_features=6)
dic = exp.__dict__
print(dic)
'''
'''
elements = l.data.drop(columns='label')
e = elements.values[0]
e2 = e.copy()
#e3 =np.concatenate((e,e2), axis = 1)
e3 = np.array([e,e2])
print(pd.DataFrame(e3))
e4 = pd.DataFrame(e)
#data = l.prep.transform(e3)
#lime_exp = l.explainer.explain_instance(data[0], l.predict_fn, num_features=6)
exp = l.get_lime_exp(l.explainer, l.predict_fn, 0, e4, num_features=6)
dic = exp.__dict__
print(dic)
dic.pop('random_state')
'''
