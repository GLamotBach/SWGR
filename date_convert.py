from datetime import date


def age_weight(iso_date):
    """Converts a iso-format date into a weight, where older dates give lesser weight"""
    acquired_date = date.fromisoformat(iso_date)
    processing_date = date.today()
    age_of_data = processing_date - acquired_date
    age_of_data = age_of_data.days + 1
    weight = 1 / age_of_data
    return weight


if __name__ == '__main__':
    print(age_weight('2024-04-14'))
    print(age_weight('2024-04-13'))
    print(age_weight('2024-04-12'))
