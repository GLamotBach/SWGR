import scrape_classes
import requests
import csv
from datetime import date
from bs4 import BeautifulSoup


def scrape_offer(offer_id):
    """Function for scraping information from a single sale offer from otomoto.pl"""
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

    # Data preparation of a single entry
    entry = [str(date.today())]

    # Car model including brand, model, generation (if it has one) and version (if it has one)
    car_model = (all_parameter_dict['Marka pojazdu'] + " " + all_parameter_dict['Model pojazdu'])
    if 'Generacja' in all_parameter_dict:
        car_model = car_model + " " + all_parameter_dict['Generacja']
    if 'Wersja' in all_parameter_dict:
        car_model = car_model + " " + all_parameter_dict['Wersja']
    entry.append(car_model)

    # Car's production date
    entry.append(int(all_parameter_dict['Rok produkcji']))

    # Car's mileage (in kilometers)
    mileage = all_parameter_dict['Przebieg']
    mileage = mileage.replace('km', '')
    mileage = mileage.replace(' ', '')
    entry.append(int(mileage))

    # Engine capacity
    engine_capacity = all_parameter_dict['Pojemność skokowa']
    engine_capacity = engine_capacity.replace('cm3', '')
    engine_capacity = engine_capacity.replace(' ', '')
    entry.append(int(engine_capacity))

    # Fuel type
    fuel_type = all_parameter_dict['Rodzaj paliwa']
    entry.append(fuel_type)

    # Engine power
    engine_power = all_parameter_dict['Moc']
    engine_power = engine_power.replace('KM', '')
    engine_power = engine_power.replace(' ', '')
    entry.append(int(engine_power))

    # Gearbox type
    gearbox = all_parameter_dict['Skrzynia biegów']
    entry.append(gearbox)

    # Drive type
    drive = all_parameter_dict['Napęd']
    drive = drive.replace(' ', '_')
    entry.append(drive)

    # Body type
    body_type = all_parameter_dict['Typ nadwozia']
    entry.append(body_type)

    # Number of doors
    doors = all_parameter_dict['Liczba drzwi']
    entry.append(doors)

    # Number of seats
    if 'Liczba miejsc' in all_parameter_dict:
        seats = all_parameter_dict['Liczba miejsc']
    else:
        # Default value of seats
        seats = 5
    entry.append(seats)

    # Paint type
    if 'Rodzaj koloru' in all_parameter_dict:
        paint_type = all_parameter_dict['Rodzaj koloru']
    else:
        # Default value of paint type
        paint_type = 'Mono'
    entry.append(paint_type)

    # Paint color
    paint_color = all_parameter_dict['Kolor']
    paint_color = paint_color.replace(' ', '_')
    entry.append(paint_color)

    # Country of origin
    if 'Kraj pochodzenia' in all_parameter_dict:
        origin = all_parameter_dict['Kraj pochodzenia']
    else:
        # Default value of "country of origin
        origin = 'Polska'
    entry.append(origin)

    # Registered in country
    if 'Zarejestrowany w Polsce' in all_parameter_dict:
        if all_parameter_dict['Zarejestrowany w Polsce'] == 'Tak':
            registered_in_country = 1
        else:
            registered_in_country = 0
    else:
        # Default value for "Registered in country"
        registered_in_country = 0
    entry.append(registered_in_country)

    # First owner
    if 'Pierwszy właściciel (od nowości)' in all_parameter_dict:
        if all_parameter_dict['Pierwszy właściciel (od nowości)'] == 'Tak':
            first_owner = 1
        else:
            first_owner = 0
    else:
        # Default value for "First owner"
        first_owner = 0
    entry.append(first_owner)

    # Did not have a collision
    if 'Bezwypadkowy' in all_parameter_dict:
        if all_parameter_dict['Bezwypadkowy'] == 'Tak':
            no_collision = 1
        else:
            no_collision = 0
    else:
        # Default value for "Did not have a collision"
        no_collision = 0
    entry.append(no_collision)

    # Serviced in authorized station
    if 'Serwisowany w ASO' in all_parameter_dict:
        if all_parameter_dict['Serwisowany w ASO'] == 'Tak':
            authorized_service = 1
        else:
            authorized_service = 0
    else:
        # Default value of serviced in authorized station
        authorized_service = 0
    entry.append(authorized_service)

    # State of the car
    state = all_parameter_dict['Stan']
    entry.append(state)

    # Additional features
    additional_features = ''
    features_section = soup.find(id=scrape_classes.features_section_id)
    features = features_section.find_all(class_=scrape_classes.features_class)
    for feature in features:
        feature = feature.text
        feature = feature.replace(' ', '_')
        additional_features = additional_features + feature + ' '
    additional_features = additional_features.strip()
    entry.append(additional_features)

    # Car price
    price = results.find(class_=scrape_classes.price_value)
    price = price.text
    price = price.replace(' ', '')
    price = price.replace(',', '.')
    price = int(float(price))
    entry.append(price)

    return entry


def save_entry(entry):
    """Saving an entry to a csv file"""
    with open('car_offers_otomoto.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(entry)


def mark_as_collected(offer_id):
    collected = [offer_id]
    with open('collected_offers.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(collected)


def collect_offer(offer_id):
    """Handling to proces of adding data from website to the dataset"""
    entry = scrape_offer(offer_id)
    mark_as_collected(offer_id)
    save_entry(entry)


def offers_in_database():
    """Returns a list of offers that are already in the dataset"""
    collected = []
    with open('collected_offers.csv', 'r') as file:
        for line in file:
            line = line.replace('\n', '')
            collected.append(line)
    return collected


def check_if_not_collected(offer_id, collected_obj=offers_in_database()):
    """Check if a given offer is yet to be added to dataset"""
    if offer_id in collected_obj:
        return False
    else:
        return True






