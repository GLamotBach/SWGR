import pandas as pd

file_path = 'car_offers_otomoto.csv'
column_names = ['date', 'car_model', 'production_date', 'mileage', 'engine_capacity', 'fuel_type', 'engine_power',
                'gearbox', 'drive_type', 'body_type', 'doors', 'seats', 'paint_type', 'paint_color', 'origin',
                'registered', 'first_owner', 'no_collision', 'authorized_service', 'state', 'additional_features',
                'price']

raw_dataset = pd.read_csv(filepath_or_buffer=file_path, names=column_names, encoding='unicode_escape')

wrong = raw_dataset[raw_dataset['engine_power'] == "5,50"]
print(wrong)

cleaned = raw_dataset.replace("8,15", 8)

wrong = cleaned[cleaned['engine_power'] == "8,15"]
print(wrong)

# cleaned.to_csv(file_path)