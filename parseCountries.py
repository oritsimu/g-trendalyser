from countries import countries

country_names = []
country_codes = []

def parse():
    
    for country in countries:
        country_names.append(country["name"])
        country_codes.append(country["code"])

    return country_names, country_codes

