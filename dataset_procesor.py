import pandas as pd
import pickle


def get_vocabulary(raw_data):
    """Constructing a set of dictionaries from the dataset, translating strings to integers."""
    string_columns = ['car_model', 'fuel_type', 'gearbox', 'drive_type', 'body_type', 'seats', 'paint_type',
                      'paint_color', 'origin', 'state']
    dictionaries = {}
    for column in string_columns:
        unique_values = raw_data[column].unique()
        column_dict = {}
        counter = 1
        for unique_value in unique_values:
            column_dict[unique_value] = counter
            counter += 1
        dictionaries[column] = column_dict
    return dictionaries


def update_dictionaries(raw_data):
    """Creates a file containing an up-to-date dictionary translating string data into integers."""
    dictionaries = get_vocabulary(raw_data)
    with open('dictionaries.pkl', 'wb') as f:
        pickle.dump(dictionaries, f)


def load_dictionaries():
    """Loads the dictionary stored in a file."""
    with open('dictionaries.pkl', 'rb') as f:
        load = pickle.load(f)
        return load


def transform_to_int(dataset):
    """Converts dataset string data into integer values according to the dictionary."""
    string_columns = ['car_model', 'fuel_type', 'gearbox', 'drive_type', 'body_type', 'seats', 'paint_type',
                      'paint_color', 'origin', 'state']
    dictionaries = load_dictionaries()
    for index in range(len(dataset)):
        for column in string_columns:
            dataset.at[index, column] = dictionaries[column][dataset[column][index]]
    return dataset


def save_processed_data(processed_data):
    """Save data to files after processing"""
    processed_data.to_csv('processed_offers.csv', sep="\t")


def process_string(string_value):
    """Preparing string values that should be floats."""
    fixed_value = string_value.replace(',', '.')
    return float(fixed_value)


def clear_strings(processed_data):
    """Cleanup of string data in preparation for processing."""
    columns = ['car_model', 'production_date', 'mileage', 'engine_capacity', 'fuel_type', 'engine_power',
               'gearbox', 'drive_type', 'body_type', 'doors', 'seats', 'paint_type', 'paint_color', 'origin',
               'registered', 'first_owner', 'no_collision', 'authorized_service', 'state', 'price', ]
    for index in range(len(processed_data)):
        for column in columns:

            if isinstance(processed_data[column][index], str):
                processed_data.at[index, column] = process_string(processed_data[column][index])
    return processed_data


def convert_obj_to_int(processed_data):
    string_columns = ['car_model', 'fuel_type', 'gearbox', 'drive_type', 'body_type', 'seats', 'paint_type',
                      'paint_color', 'origin', 'state']
    for column in string_columns:
        processed_data[column] = processed_data[column].astype(object).astype(int)
    return processed_data


if __name__ == "__main__":

    # Importing data from csv file
    file_path = 'car_offers_otomoto.csv'
    column_names = ['date', 'car_model', 'production_date', 'mileage', 'engine_capacity', 'fuel_type', 'engine_power',
                    'gearbox', 'drive_type', 'body_type', 'doors', 'seats', 'paint_type', 'paint_color', 'origin',
                    'registered', 'first_owner', 'no_collision', 'authorized_service', 'state', 'additional_features',
                    'price']

    raw_dataset = pd.read_csv(filepath_or_buffer=file_path,
                              names=column_names,
                              encoding='ANSI',
                              index_col=False)

    # TEMP: Drop 'additional_features'
    raw_dataset = raw_dataset.drop('additional_features', axis=1)

    # TEMP: Drop 'date'
    raw_dataset = raw_dataset.drop('date', axis=1)

    update_dictionaries(raw_dataset)
    data_processed = transform_to_int(raw_dataset)
    data_processed = clear_strings(data_processed)
    data_processed = convert_obj_to_int(data_processed)

    # Saving processed data
    save_processed_data(data_processed)

    # Confirmation
    print(data_processed.dtypes)
    print('Dataset processed')

