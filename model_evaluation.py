# Script for running an evaluation of a trained model.
import keras
import tensorflow as tf
import pandas as pd
# from model import test_labels, test_features

# Load data
file_path = 'processed_offers_b.csv'
column_names = ['car_model', 'production_date', 'mileage', 'engine_capacity', 'fuel_type', 'engine_power',
                'gearbox', 'drive_type', 'body_type', 'doors', 'seats', 'paint_type', 'paint_color', 'origin',
                'registered', 'first_owner', 'no_collision', 'authorized_service', 'state', 'price', ]

raw_dataset = pd.read_csv(filepath_or_buffer=file_path,
                          names=column_names,
                          encoding='unicode_escape',
                          header=1,
                          sep='\t')

dataset = raw_dataset.copy()

# Load trained model
loaded_model = tf.keras.models.load_model('dnn_model.keras')

# Evaluation
