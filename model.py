import keras
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers


def build_and_compile_model(norm):
    """Function that handles the creation and training of the model."""
    model = keras.Sequential([
        norm,
        layers.Dense(128, activation='relu', input_shape=(19,)),
        layers.Dense(128, activation='relu'),
        layers.Dense(1)
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mean_absolute_error')
    return model


# Normalization
normalizer = tf.keras.layers.Normalization(axis=-1, input_shape=(19,))

if __name__ == "__main__":
    # Importing data from csv file
    file_path = 'processed_offers.csv'
    column_names = ['car_model', 'production_date', 'mileage', 'engine_capacity', 'fuel_type', 'engine_power',
                    'gearbox', 'drive_type', 'body_type', 'doors', 'seats', 'paint_type', 'paint_color', 'origin',
                    'registered', 'first_owner', 'no_collision', 'authorized_service', 'state', 'price', ]

    raw_dataset = pd.read_csv(filepath_or_buffer=file_path,
                              names=column_names,
                              encoding='unicode_escape',
                              header=1,
                              sep='\t')

    dataset = raw_dataset.copy()

    # Inspect data for missing values

    missing_values = dataset.isna().sum()
    print(f"Dataframe size: {dataset.size / len(column_names)}")
    print(f"Missing values: \n{missing_values}")

    # Splitting data into training and test sets

    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    # Splitting features from labels

    train_features = train_dataset.copy()
    test_features = test_dataset.copy()

    train_labels = train_features.pop('price')
    test_labels = test_features.pop('price')

    train_features = np.asarray(train_features.copy()).astype('float32')
    normalizer.adapt(np.array(train_features))

    print(normalizer.mean.numpy())

    # Regression with DNN
    dnn_model = build_and_compile_model(normalizer)
    dnn_model.summary()

    history = dnn_model.fit(
        train_features,
        train_labels,
        epochs=200,
        verbose=1,
        validation_split=0.2)

    # Results of test set
    test_results = dnn_model.evaluate(test_features, test_labels, verbose=1)
    print(f"Model evaluation: {test_results}")

    # Test predictions
    test_predictions = dnn_model.predict(test_features).flatten()

    print(type(test_labels))
    print(type(test_predictions))

    print("Test predictions:")
    deviations = []
    for i in range(len(test_labels)):
        target = test_labels.iloc[i]
        prediction = test_predictions[i]
        percentage_deviation = round((abs(target - prediction) / target) * 100, 2)
        deviations.append(percentage_deviation)
        print(f"{target} - predicted: {prediction} - Deviation: {percentage_deviation}")

    deviation_mean = round(sum(deviations) / len(deviations), 2)
    print(f"Predictions deviation: {deviation_mean}%")

    # Saving the trained model
    dnn_model.save('dnn_model.keras')

