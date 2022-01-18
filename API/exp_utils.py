
import shap
import pandas as pd
from DataLoader_ey import preprocessX, data_loader
from tensorflow.keras.models import load_model

# Load the dataset and the explainer in the main app at start up (make dependet from chosen method)
def create_shap_explainer():
    data = data_loader()
    data = preprocessX(data)
    model = load_model('smote_ey.tf')
    X_df = pd.DataFrame(data.reshape((-1,18)), columns=data.columns)
    # TODO continue here

    

def shap_explanation(explainer: shap.KernelExplainer, instance):
    return explainer.shap_values(instance, nsamples="auto", l1_reg="num_features(7)") # TODO check which num_features to use

