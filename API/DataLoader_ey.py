import pandas as pd
import pickle
from pandas.core.frame import DataFrame
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np


def data_loader(path='Data/german.csv', raw=False, remove_outliers=True):
    """
    Loads the german credit data
    :param raw: If true, reads the raw dataframe, else it removes columns unused for training
    :param path: Path to file
    :return: dataframe
    """
    df = pd.read_csv(path, index_col=0)

    if raw:
        return df
    else:
        # Create numeric label variable for investigation and model building
        df['label'] = df['classification_'].map({'Approved': 0, 'Rejected': 1})
        # Drop unnecessary columns
        #df.drop(columns=['other_debtors_', 'people_liable_', 'classification_', 'Unnamed: 0'], inplace=True)
        df.drop(columns=['foreign_worker_', 'status_sex_', 'classification_'], inplace=True)
        # Change categories of previous_loans variable
        df['previous_loans_'].replace(['4 or 5', '6 or more'], '4 or more', inplace=True)

        if remove_outliers:
            # Identify thresholds for outliers
            IQR = df['amount_'].quantile(0.75) - df['amount_'].quantile(0.25)
            upper_limit_3iqr = df['amount_'].quantile(0.75) + 3 * IQR
            df.loc[df['amount_'] > upper_limit_3iqr, 'amount_'] = upper_limit_3iqr

        return df

#preprocessing steps from German_Credit_NN_final_ey
def preprocessX(df):
    X = df.drop(columns='label')

    from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
    from sklearn.compose import ColumnTransformer


    cat_cols = X.select_dtypes(include=['object', 'category']).columns.to_list()
    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.to_list()


    preprocessor = ColumnTransformer(
                transformers=[('num', MinMaxScaler(), num_cols),
                            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)]
            )

    preprocessor.fit_transform(X)
    X = preprocessor.transform(X)
    return X

def createDataframeForDB(deleteLabel=True):
    df = data_loader()
    data = preprocessX(df)
    model = load_model('smote_ey.tf')
    results = model.predict(data)
    recommendation = []

    for i in range(results.size):
        if results[i] >= 0.5:
            recommendation.append('Reject')
        else:
            results[i] = 1 - results[i]
            recommendation.append('Approve')
            
    df['NN_confidence'] = results
    df['NN_recommendation']= np.array(recommendation)
    if (deleteLabel):
        df.drop(columns='label', inplace=True)

    return df



