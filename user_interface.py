from check_offer import get_offer_data_url
import numpy as np
import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model('dnn_model.keras')


# Input data for prediction
offer_url = input("otomoto.pl offer URL:\n")
offer_data = get_offer_data_url(offer_url)
offer_data_array = np.array(offer_data)

# Make a prediction based on acquired from otomoto.pl offer
prediction = model.predict(offer_data_array)

# Return the prediction
print(prediction)

