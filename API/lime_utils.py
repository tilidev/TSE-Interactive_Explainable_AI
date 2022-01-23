import pandas as pd
import numpy as np
import lime
import lime.lime_tabular
from tensorflow.keras.models import load_model
from DataLoader_ey import data_loader 
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from constants import rename_dict, AttributeNames, lime_exp_mapping
import json

class LimeHelper():
    """Class for Lime Explanations.
    Uses code from xai_reference
    """
    def __init__(self):
        """Initializes the LimeHelper() for usage by the API
        Fits a preprocessor and lime explainer
        """
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
        """Prediction function for lime explainer
        :param X: should be the data without the column label
        """
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
        Function to preprocess the given instance data for the lime explainer
        :param X_df: should be a pandas dataframe containing 18 attributes
        :return: label encoded data 
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

    def get_lime_exp(self, explainer, prediction_function, instance_df, **kwargs):
        """Method to get the lime explanation
        :param instance_df: dataframe with instance information
        :return lime explanation object:
        """
        data_le = self.preprocess_new_data(instance_df)
        lime_exp = explainer.explain_instance(data_le.values[0], prediction_function, **kwargs)
        return lime_exp
    
    def get_api_response(self,instance, num_features=6):
        """
        Method that can be called by the API after initializing the LimeHelper
        :param instance: given Instance info, should be in json format
        :return: a lime explanation json with the keys predict_proba and explanations
        Predict_proba contains an array with probabilities for approve and reject
        Explanations contains a dict where the keys are the attribute names 
        """
        instance_df = pd.DataFrame(instance, index = [0])
        instance_df.drop(columns=[AttributeNames.ident.value,AttributeNames.NN_recommendation.value,AttributeNames.NN_confidence.value], inplace=True)
        exp = self.get_lime_exp(self.explainer, self.predict_fn,instance_df, num_features)
        exp_dict = exp.__dict__
        #exp_dict also contains keys random_state,mode,domain_mapper,intercepts,score,local_pred,class_names,top_labels that are not needed
        local_exp = exp_dict['local_exp']
        predict_proba = exp_dict['predict_proba'] # numpy array containing probability for approve and reject
        local_exp_list = local_exp[1] #get list with explanation tuples from dict
        #create explanation dict with attribute names instead of numbers as keys
        explanations = {}
        for tuple in local_exp_list:
            explanations[lime_exp_mapping[tuple[0]]] = tuple[1]
        return_dict = {}
        return_dict['predict_proba'] = predict_proba
        return_dict['explanations'] = explanations
        return_json = json.dumps(return_dict)
        return json.loads(return_json)
        




