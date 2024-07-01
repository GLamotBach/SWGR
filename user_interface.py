from check_offer import get_offer_data_url
import numpy as np
import tensorflow as tf


def appraise_offer(offer_url):
    """Returns an appraised value of a car based on a URL of an otomoto.pl sale offer."""
    model = tf.keras.models.load_model('dnn_model.keras')
    offer_data = get_offer_data_url(offer_url)
    offer_data_array = np.array(offer_data)
    prediction = model.predict(offer_data_array)
    return prediction[0][0]


def appraise_offer_approx(offer_url):
    """Returns an approximated, appraised value of a car based on a URL of an otomoto.pl sale offer."""
    return int(round(appraise_offer(offer_url)))

# # Load trained model
# model = tf.keras.models.load_model('dnn_model.keras')
#
#
# # Input data for prediction
# offer_url = input("otomoto.pl offer URL:\n")
# offer_data = get_offer_data_url(offer_url)
# offer_data_array = np.array(offer_data)
#
# # Make a prediction based on acquired from otomoto.pl offer
# prediction = model.predict(offer_data_array)
#
# # Return the prediction
# print(prediction)
if __name__ == "__main__":
    print(appraise_offer("https://www.otomoto.pl/osobowe/oferta/opel-corsa-opel-corsa-1-4-ID6Gvheg.html"))
    print(appraise_offer_approx("https://www.otomoto.pl/osobowe/oferta/opel-corsa-opel-corsa-1-4-ID6Gvheg.html"))