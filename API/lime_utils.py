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

# Read credit data
data = data_loader()
# Load tensorflow model
model = load_model('smote_ey.tf')

def data_prep(data):
    #steps from data_preprocess
    
    #TODO needs to be adapted to AttributeNames
    rename_dict = {
        'balance_': 'Account Balance',
        'duration_': 'Duration (months)',
        'history_': 'Loan History',
        'purpose_': 'Purpose',
        'amount_': 'Amount (EUR)',
        'savings_': 'Savings Account',
        'employment_': 'Employment',
        'available_income_': 'Available Income',
        'other_debtors_': 'Guarantee',
        #'status_sex_': 'Personal Status / Sex',
        'residence_': 'Residence Duration',
        'assets_': 'Assets',
        'age_': 'Age (years)',
        'other_loans_': 'Other Loans',
        'housing_': 'Housing',
        'previous_loans_': 'Number of Previous Loans',
        'job_': 'Job',
        'people_liable_': 'Number of dependents',
        'telephone_': 'Telephone',
        #'foreign_worker_': 'Foreign Worker'
    }
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
    return preprocessor_le, X_train, cat_names, cat_indices, feature_names,X

prep,X_train,cat_names,cat_indices,feature_names,X =data_prep(data)

def predict_fn(X):
    # Single data point has dimensions (18,) but (1, 18) is needed for preprocessing
    # Therefore, reshape input to (-1, 18)
    X_df = pd.DataFrame(X.reshape((-1, 18)), columns=X_train.columns)
    # Preprocess input and create nd-array
    X_transformed = prep.transform(X_df).toarray()
    # model.predict output has shape (n, 1) but (n,) is needed
    prob = model.predict(X_transformed).reshape(-1, )
    # Return predictions in correct format, dim = (n, 2), note that the first entry
    # has to represent P(y=0 | X)
    proba_predictions = np.array([1 - prob, prob]).transpose()
    return proba_predictions

def preprocess_new_data(X_df):
        """
        Function to preprocess new data for LIME and anchor explanations
        :param X_df:
        :return:
        """
        data = X_df.copy()
        # List of feature names
        feature_names = X.columns.to_list()

        # Lists of categorical and numerical feature names (needed for preprocessing)
        cat_cols = X.select_dtypes(include=['object', 'category']).columns.to_list()

        # List of indices of categorical features
        cat_indices = [feature_names.index(col) for col in cat_cols]

        # Label encoding
        
        for cat_idx in cat_indices:
            # Fit label encoder on training data and transform respective column
            le = LabelEncoder()
            le.fit(X.iloc[:, cat_idx])
            data.iloc[:, cat_idx] = le.transform(data.iloc[:, cat_idx])
        print(data)
        return data

def get_lime_exp(explainer, prediction_function, idx, data_source, visualize=True, **kwargs):
    data_le = preprocess_new_data(data_source)
    print(data_le.values[idx])
    lime_exp = explainer.explain_instance(data_le.values[idx], prediction_function, **kwargs)
    if visualize:
            lime_exp.show_in_notebook(show_all=False)
    return lime_exp

lime_explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values, feature_names=feature_names,
                                                   class_names=['Approved', 'Rejected'],
                                                   discretize_continuous=True, mode='classification',
                                                   categorical_features=cat_indices, categorical_names=cat_names,
                                                   feature_selection='lasso_path' )


exp = get_lime_exp(lime_explainer, predict_fn, 0, data.drop(columns='label'), num_features=6)
print(exp.__dict__)
