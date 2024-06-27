import scrape_classes
from offer_id import extract_offer_id
# from dataset_procesor import load_dictionaries
import requests
import pickle
from datetime import date
from bs4 import BeautifulSoup


def load_dictionaries():
    """Loads the dictionary stored in a file."""
    with open('dictionaries.pkl', 'rb') as f:
        load = pickle.load(f)
        return load
# Pickle gubi polskie znaki


def retrieve_offer(offer_id: str) -> list:
    """Retrieve information from an offer from otomoto.pl for price prediction."""
    # Simular to scrape_offer() from scraper_otomoto.py but different.
    # scrape_offer() - should drop incomplete offers.
    # retrieve_offer() - must work even with incomplete offers.
    # Dumb default values for missing information - Most probable values for all cars in general.
    # TODO: Implement a functionality that will assume probable default missing values based on the model of the car

    # Retrieving data from site
    url = "https://www.otomoto.pl/osobowe/oferta/" + offer_id + ".html"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="__next")

    parameters = results.find_all(class_=scrape_classes.parameters_class)
    all_parameter_dict = {}
    for para in parameters:
        parameter = para.find(class_=scrape_classes.parameter_class)
        parameter = parameter.text
        value_a = para.find(class_=scrape_classes.parameter_value_text)
        value_b = para.find(class_=scrape_classes.parameter_value_link)
        if value_a:
            value = value_a.text
            all_parameter_dict[parameter] = value
        elif value_b:
            value = value_b.text
            all_parameter_dict[parameter] = value

    # Data preparation of a single check
    check = [str(date.today())]

    # Car model including brand, model, generation (if it has one) and version (if it has one)
    car_model = (all_parameter_dict['Marka pojazdu'] + " " + all_parameter_dict['Model pojazdu'])
    if 'Generacja' in all_parameter_dict:
        car_model = car_model + " " + all_parameter_dict['Generacja']
    if 'Wersja' in all_parameter_dict:
        car_model = car_model + " " + all_parameter_dict['Wersja']
    check.append(car_model)

    # Car's production date
    if 'Rok produkcji' in all_parameter_dict:
        production_date = int(all_parameter_dict['Rok produkcji'])
    else:
        production_date = date.today().year
    check.append(production_date)

    # Car's mileage (in kilometers)
    if 'Przebieg' in all_parameter_dict:
        mileage = all_parameter_dict['Przebieg']
        mileage = mileage.replace('km', '')
        mileage = mileage.replace(' ', '')
    else:
        mileage = 1
    check.append(int(mileage))

    # Engine capacity
    if 'Pojemność skokowa' in all_parameter_dict:
        engine_capacity = all_parameter_dict['Pojemność skokowa']
        engine_capacity = engine_capacity.replace('cm3', '')
        engine_capacity = engine_capacity.replace(' ', '')
    else:
        engine_capacity = 1400
    check.append(int(engine_capacity))

    # Fuel type
    if 'Rodzaj paliwa' in all_parameter_dict:
        fuel_type = all_parameter_dict['Rodzaj paliwa']
    else:
        fuel_type = 'Benzyna'
    check.append(fuel_type)

    # Engine power
    if 'Moc' in all_parameter_dict:
        engine_power = all_parameter_dict['Moc']
        engine_power = engine_power.replace('KM', '')
        engine_power = engine_power.replace(' ', '')
    else:
        engine_power = 100
    check.append(int(engine_power))

    # Gearbox type
    if 'Skrzynia biegów' in all_parameter_dict:
        gearbox = all_parameter_dict['Skrzynia biegów']
    else:
        gearbox = 'Manualna'
    check.append(gearbox)

    # Drive type
    if 'Napęd' in all_parameter_dict:
        drive = all_parameter_dict['Napęd']
        drive = drive.replace(' ', '_')
    else:
        drive = 'Na_przednie_koła'
    check.append(drive)

    # Body type
    if 'Typ nadwozia' in all_parameter_dict:
        body_type = all_parameter_dict['Typ nadwozia']
    else:
        body_type = 'Kombi'
    check.append(body_type)

    # Number of doors
    if 'Liczba drzwi' in all_parameter_dict:
        doors = all_parameter_dict['Liczba drzwi']
    else:
        doors = 5
    check.append(int(doors))

    # Number of seats
    if 'Liczba miejsc' in all_parameter_dict:
        seats = all_parameter_dict['Liczba miejsc']
    else:
        # Default value of seats
        seats = 5
    check.append(int(seats))

    # Paint type
    if 'Rodzaj koloru' in all_parameter_dict:
        paint_type = all_parameter_dict['Rodzaj koloru']
    else:
        # Default value of paint type
        paint_type = 'Mono'
    check.append(paint_type)

    # Paint color
    if 'Rodzaj koloru' in all_parameter_dict:
        paint_color = all_parameter_dict['Kolor']
        paint_color = paint_color.replace(' ', '_')
    else:
        paint_color = 'Szary'
    check.append(paint_color)

    # Country of origin
    if 'Kraj pochodzenia' in all_parameter_dict:
        origin = all_parameter_dict['Kraj pochodzenia']
    else:
        # Default value of "country of origin
        origin = 'Polska'
    check.append(origin)

    # Registered in country
    if 'Zarejestrowany w Polsce' in all_parameter_dict:
        if all_parameter_dict['Zarejestrowany w Polsce'] == 'Tak':
            registered_in_country = 1
        else:
            registered_in_country = 0
    else:
        # Default value for "Registered in country"
        registered_in_country = 0
    check.append(registered_in_country)

    # First owner
    if 'Pierwszy właściciel (od nowości)' in all_parameter_dict:
        if all_parameter_dict['Pierwszy właściciel (od nowości)'] == 'Tak':
            first_owner = 1
        else:
            first_owner = 0
    else:
        # Default value for "First owner"
        first_owner = 0
    check.append(first_owner)

    # Did not have a collision
    if 'Bezwypadkowy' in all_parameter_dict:
        if all_parameter_dict['Bezwypadkowy'] == 'Tak':
            no_collision = 1
        else:
            no_collision = 0
    else:
        # Default value for "Did not have a collision"
        no_collision = 0
    check.append(no_collision)

    # Serviced in authorized station
    if 'Serwisowany w ASO' in all_parameter_dict:
        if all_parameter_dict['Serwisowany w ASO'] == 'Tak':
            authorized_service = 1
        else:
            authorized_service = 0
    else:
        # Default value of serviced in authorized station
        authorized_service = 0
    check.append(authorized_service)

    # State of the car
    if 'Stan' in all_parameter_dict:
        state = all_parameter_dict['Stan']
    else:
        state = 'Używane'
    check.append(state)

    # Additional features
    additional_features = ''
    features_section = soup.find(id=scrape_classes.features_section_id)
    features = features_section.find_all(class_=scrape_classes.features_class)
    if features:
        for feature in features:
            feature = feature.text
            feature = feature.replace(' ', '_')
            additional_features = additional_features + feature + ' '
        additional_features = additional_features.strip()
    else:
        additional_features = ''
    check.append(additional_features)

    # Car price
    price = results.find(class_=scrape_classes.price_value)
    price = price.text
    price = price.replace(' ', '')
    price = price.replace(',', '.')
    price = int(float(price))
    check.append(price)

    return check


def drop_unused_features(check: list) -> list:
    """Temporary function that removes features not yet used in this version of the model."""
    check = check[1:-2]
    return check


def transform_list_str_to_int(check: list) -> list:
    """Converts lists string data into integer values according to the dictionary."""
    string_columns = ['car_model', 'fuel_type', 'gearbox', 'drive_type', 'body_type', 'seats', 'paint_type',
                      'paint_color', 'origin', 'state']
    string_indexes = [0, 4, 6, 7, 8, 10, 11, 12, 13, 18]
    dictionaries = load_dictionaries()
    next_value_to_change = 0
    for i in range(len(check)):
        if i in string_indexes:
            features_value = check[i]
            feature_column = string_columns[next_value_to_change]
            check[i] = dictionaries[feature_column][features_value]
            next_value_to_change += 1
    return check


def get_offer_data_id(offer_id: str) -> list:
    """Returns a model-readable data from a otomoto.pl offer ID"""
    offer_data = retrieve_offer(offer_id)
    offer_data = drop_unused_features(offer_data)
    offer_data = transform_list_str_to_int(offer_data)
    return offer_data


def get_offer_data_url(offer_url: str) -> list:
    """Returns a model-readable data from a otomoto.pl offer URL"""
    offer_id = extract_offer_id(offer_url)
    offer_data = get_offer_data_id(offer_id)
    return offer_data


if __name__ == "__main__":
    # offer_1 = "ID6Grb4z"
    offer_1 = "ID6GvnzN"
    offer_d = retrieve_offer(offer_1)
    used_offer_data = drop_unused_features(offer_d)
    # used_offer_data[0] = 'Volkswagen Passat B5 FL (2000-2005)'
    transformed_data = transform_list_str_to_int(used_offer_data)
    print(offer_d)
    print(used_offer_data)
    print(transformed_data)
    print(f"Len: {len(transformed_data)}")
    # dict = load_dictionaries()
    # print(dict['drive_type'])
    # print(dict['drive_type']['Na_przednie_koła'])
    # print(dict['car_model'][used_offer_data[0]])
    # print(dict['seats'])
    print(get_offer_data_url('https://www.otomoto.pl/osobowe/oferta/mercedes-benz-klasa-e-mercedes-w-124-500e-1991r-stan-igla-ID6Guynh.html'))
