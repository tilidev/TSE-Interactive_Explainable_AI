import dice_ml
from tensorflow.python.keras.saving.save import load_model
from DataLoader_ey import data_loader
import tensorflow as tf


data = data_loader('Data/german.csv')

backend = 'TF2'
model = load_model('smote_ey.tf')

d = dice_ml.Data(data)



