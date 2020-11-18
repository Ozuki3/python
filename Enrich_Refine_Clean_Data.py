import json
import requests

ENDPOINT = 'https://swapi.co/api'

PERSON_KEYS = ('url', 'name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld', 'species')
PLANET_KEYS = ('url', 'name', 'rotation_period', 'orbital_period', 'diameter', 'climate', 'gravity', 'terrain', 'surface_water', 'population')
PLANET_HOTH_KEYS = ('url', 'name', 'system_position', 'natural_satellites', 'rotation_period', 'orbital_period', 'diameter', 'climate', 'gravity', 'terrain', 'surface_water', 'population', 'indigenous_life_forms')
STARSHIP_KEYS = ('url', 'starship_class', 'name','model', 'manufacturer', 'length', 'width', 'max_atmosphering_speed', 'hyperdrive_rating', 'MGLT', 'crew', 'passengers', 'cargo_capacity', 'consumables', 'armament')
VEHICLE_KEYS = ('url', 'vehicle_class', 'name', 'model', 'manufacturer', 'length', 'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity', 'consumables', 'armament')
SPECIES_KEYS = ('url', 'name', 'classification', 'designation','average_height', 'skin_colors', 'hair_colors', 'eye_colors', 'average_lifespan', 'language')

def assign_crew(starship, crew): 
    """Assigning crew's key-value pairs to startship (and using crew values replacing starship values on matching keys)

    Parameters:
        starship(dict): a dictionary from the provided local json file.
        crew(dict): a dictionary with 2 key-value pairs.

    Returns:
        new_starship(dict): updated starship dictionary that includes key-value pairs of crew dictionary.
    """
    new_startship = {**starship, **crew}
    return new_startship

def clean_data(entity):
    """Calling other functions to converting the values of the 'entity' into requested type, if its keys in the 'props' sequences, and then change the 'unknown' and 'n/a' into 'null'.
        For the dict_props, firstly getting the resource from SWAPI and filter it; secondely converting types of its values.

    Parameters:
        entity(dict): a dictionary with dirty data which needs to be cleaned.

    Returns:
        cleaned(dict): cleaned data dictionary
    """
    int_props = ('height','mass','rotation_period', 'orbital_period', 'diameter', 'surface_water', 'population', 'average_height','average_lifespan','max_atmosphering_speed', 'MGLT', 'crew', 'passengers', 'cargo_capacity')
    float_props = ('gravity', 'length', 'width', 'hyperdrive_rating') #gravity width
    list_props = ('hair_color', 'skin_color', 'climate', 'terrain', 'eye_colors', 'skin_colors', 'hair_colors')
    dict_props = ('homeworld', 'species')
    cleaned = {}
    for key in entity.keys():
        if key in int_props:
            cleaned[key] = convert_string_to_int(entity[key])
        elif key in float_props:
            if key == "gravity":
                temp = entity[key].split()
                if len(temp) > 1:
                    entity[key] = temp[0]
            cleaned[key] = convert_string_to_float(entity[key])
        elif key in list_props:
            cleaned[key] = convert_string_to_list(entity[key])
            if is_unknown(cleaned[key][0]) == True:
                cleaned[key] = None
        elif key in dict_props: 
            if key == 'homeworld':
                api_data = get_swapi_resource(entity[key], params = None) 
                api_data = filter_data(api_data, PLANET_KEYS)
            else:
                api_data = get_swapi_resource(entity[key][0], params = None) 
                api_data = filter_data(api_data, SPECIES_KEYS)
            cleaned_api = {}
            for key_api in api_data.keys():
                if key_api in int_props:
                    cleaned_api[key_api] = convert_string_to_int(api_data[key_api])
                elif key_api in float_props:
                    if key_api == "gravity":
                        temp = api_data[key_api].split()
                        if len(temp) > 1:
                            api_data[key_api] = temp[0]
                    cleaned_api[key_api] = convert_string_to_float(api_data[key_api])
                elif key_api in list_props:
                    cleaned_api[key_api] = convert_string_to_list(api_data[key_api])
                    if is_unknown(cleaned_api[key_api][0]) == True:
                        cleaned_api[key_api] = None
                else:
                    cleaned_api[key_api] = api_data[key_api]
            for key_api in api_data.keys():
                if is_unknown(api_data[key_api]) == True:
                    cleaned_api[key_api] = None
            if key == 'homeworld':
                cleaned[key] = cleaned_api
            else:
                cleaned[key] = [cleaned_api]
        else:
            cleaned[key] = entity[key]
    for key in entity.keys():
        if is_unknown(entity[key])==True:
            cleaned[key] = None
    return cleaned  

def combine_data(default_data, override_data):
    """Combining default_data and override_data and using override values replacing default values on matching keys.

    Parameters:
        default_data(dict): a dictionary from the provided local json file.
        override_data(dict): a dictionary from the SWAPI

    Returns:
        combined(dict): a dictionary that combines the key-value pairs of both the default dictionary and the override dictionary, with override values replacing default values on matching keys.
    """
    combined = {}
    for key in default_data.keys():
        if key in override_data.keys():
            combined[key] = override_data[key]
        elif key not in override_data.keys():
            combined[key] = default_data[key]
    for key in override_data.keys(): 
        if key not in default_data.keys():
            combined[key] = override_data[key]
    return combined

def convert_string_to_float(value):
    """Converting the given string to a float.

    Parameters:
        value(str): a string.

    Returns:
        value(float)
    """
    try:
        return float(value)
    except ValueError:
        return value

def convert_string_to_int(value):
    """Converting the given string to an int.

    Parameters:
        value(str): a string.

    Returns:
        value(int)
    """
    try:
        return int(value)
    except ValueError:
        return value

def convert_string_to_list(value, delimiter=', '):
    """Converting the given string to an list.

    Parameters:
        value(str): a string.
        delimiter: using it to split the given string.

    Returns:
        value(list)
    """
    try:
        new_value = value.split(delimiter)
        return new_value
    except ValueError:
        return value

def filter_data(data, filter_keys):  
    """Applying a key name filter to a dictionary in order to return an ordered and requested subset of key-values.
    
    Parameters:
        data(dict): A dictionary with disordered key-value pairs. 
        filter_keys(tuple): Given ordered key sequence.
    
    Returns:
        result(dict): filtered key-value pairs to the given ordered key sequence.
    """ 
    result = {}
    for key in filter_keys:
        if key in data.keys():
            result[key] = data[key]
    return result

def get_swapi_resource(url, params = None): 
    """Initiates an HTTP GET request to the SWAPI in order to return resource in the given url.
    
    Parameters:
        url(str): the location of the resource
        params(dict): optional query of {key:value} pairs may be provided as search terms.
    
    Returns:
        response(dict): SWAPI data is serialized as JSON and dictionary representations of the decoded JSON document.
    """
    response = requests.get(url, params).json() 
    return response

def is_unknown(value): 
    """Applying a case-insensitive truth value test for a given value.
    
    Parameters:
        value(str): a given value which will be removed whitespaces around it and changed into lower case before the truth test.
    
    Returns:
        Return true if it equals unknown or n/a and return false if not.
    """
    UNKNOWN = ["unknown", "n/a"]
    if str(value).strip().lower() in UNKNOWN:
        return True 
    else:
        return False

def read_json(filepath):
    """Given a valid filepath reads a JSON document and returns a dictionary.
    
    Parameters:
        filepath (str): path to file.
    
    Returns:
        dict: dictionary representations of the decoded JSON document.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json(filepath, data):
    """Given a valid filepath writes data to a JSON file.

    Parameters:
        filepath (str): path to file.
        data: the data will be encoded as JSON and written to the file.

    Returns:
        None
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    """Entry point. This program will interact with local file assets and the Star Wars
    API to create two data files required by Rebel Alliance Intelligence.

    - A JSON file comprising a list of likely uninhabited planets where a new rebel base could be
      situated if Imperial forces discover the location of Echo Base.

    - A JSON file of Echo Base information including an evacuation plan of base personnel
      along with passenger assignments for Princess Leia, the communications droid C-3PO aboard
      the transport Bright Hope escorted by two X-wing starfighters piloted by Luke Skywalker
      (with astromech droid R2-D2) and Wedge Antilles (with astromech droid R5-D4).

    Parameters:
        None

    Returns:
        None
    """
#json1:
    planet_list = read_json('swapi_planets-v1p0.json')
    uninhabited_planet = []
    for planet in planet_list:
        if is_unknown(planet['population']) == True:
            cleaned_planet = clean_data(planet)
            filtered_planet = filter_data(cleaned_planet, PLANET_KEYS)
            uninhabited_planet.append(filtered_planet)
    write_json('swapi_planets_uninhabited-v1p1.json', uninhabited_planet)

#json2:
    echo_base = read_json('swapi_echo_base-v1p0.json') 
    #enrich hoth
    swapi_hoth = get_swapi_resource('https://swapi.co/api/planets/', params = {'search': 'Hoth'})['results'][0]
    echo_base_hoth = echo_base['location']['planet'] 
    hoth = combine_data(echo_base_hoth, swapi_hoth)
    hoth = clean_data(hoth)
    hoth = filter_data(hoth, PLANET_HOTH_KEYS)
    echo_base['location']['planet'] = hoth
    #enrich commander-Carlist_Rieekan 
    echo_base_commander = echo_base['garrison']['commander']
    echo_base_commander = clean_data(echo_base_commander)
    echo_base['garrison']['commander'] = echo_base_commander
    #enrich smuggler-Dash Rendar 
    echo_base_smuggler = echo_base['visiting_starships']['freighters'][1]['pilot']
    echo_base_smuggler = clean_data(echo_base_smuggler)
    echo_base['visiting_starships']['freighters'][1]['pilot'] = echo_base_smuggler
    #enrich snowspeeder - snowspeeders is a list
    swapi_snowspeeder = get_swapi_resource('https://swapi.co/api/vehicles/', params = {'search': 'snowspeeder'})['results'][0]
    echo_base_snowspeeder = echo_base['vehicle_assets']['snowspeeders'][0]['type'] 
    snowspeeder = combine_data(echo_base_snowspeeder, swapi_snowspeeder)
    snowspeeder = clean_data(snowspeeder)
    snowspeeder = filter_data(snowspeeder, VEHICLE_KEYS)
    echo_base['vehicle_assets']['snowspeeders'][0]['type'] = snowspeeder
    #enrich starfighters-"X-wing"
    swapi_starfighters = get_swapi_resource('https://swapi.co/api/starships/', params = {'search': 'T-65 X-wing'})['results'][0]
    echo_base_starfighters = echo_base['starship_assets']['starfighters'][0]['type'] 
    starfighters = combine_data(echo_base_starfighters, swapi_starfighters)
    starfighters = clean_data(starfighters)
    starfighters = filter_data(starfighters, STARSHIP_KEYS)
    echo_base['starship_assets']['starfighters'][0]['type'] = starfighters
    #enrich transports - GR-75
    swapi_transports = get_swapi_resource('https://swapi.co/api/starships/', params = {'search': 'GR-75 medium transport'})['results'][0]
    echo_base_transports = echo_base['starship_assets']['transports'][0]['type'] 
    transports = combine_data(echo_base_transports, swapi_transports)
    transports = clean_data(transports)
    transports = filter_data(transports, STARSHIP_KEYS)
    echo_base['starship_assets']['transports'][0]['type'] = transports
    #enrich Millennium Falcon
    swapi_freighters = get_swapi_resource('https://swapi.co/api/starships/', params = {'search': 'Millennium Falcon'})['results'][0]
    echo_base_freighters = echo_base['visiting_starships']['freighters'][0]
    freighters = combine_data(echo_base_freighters, swapi_freighters)
    freighters = clean_data(freighters)
    freighters = filter_data(freighters, STARSHIP_KEYS)
    echo_base['visiting_starships']['freighters'][0] = freighters
    # Assign crew to m_falcon
    han = get_swapi_resource('https://swapi.co/api/people/', {'search': 'Han Solo'})['results'][0]
    han = clean_data(han)
    han = filter_data(han, PERSON_KEYS)
    chewbacca = get_swapi_resource('https://swapi.co/api/people/', {'search': 'Chewbacca'})['results'][0]
    chewbacca = clean_data(chewbacca)
    chewbacca = filter_data(chewbacca, PERSON_KEYS)
    echo_base['visiting_starships']['freighters'][0] = assign_crew(freighters, {'pilot': han, 'copilot': chewbacca})

    #Update evacuation plan
    #calculation
    evac_plan = echo_base['evacuation_plan']
    personnel = 0
    for value in echo_base['garrison']['personnel'].values():
        personnel += value 
    evac_plan['max_base_personnel'] = personnel
    evac_plan['max_available_transports'] = echo_base['starship_assets']['transports'][0]['num_available']
    evac_plan['max_passenger_overload_capacity'] = evac_plan['passenger_overload_multiplier'] * evac_plan['max_available_transports'] * transports['passengers']
    #Bright hope 
    evac_transport = transports.copy()
    evac_transport['name'] = 'Bright Hope'
    # assign passenger 
    evac_transport['passenger_manifest'] = []
    leia = get_swapi_resource('https://swapi.co/api/people/', {'search': 'Leia Organa'})['results'][0]
    leia = clean_data(leia)
    leia = filter_data(leia, PERSON_KEYS)
    c_3po = get_swapi_resource('https://swapi.co/api/people/', {'search': 'C-3PO'})['results'][0]
    c_3po = clean_data(c_3po)
    c_3po = filter_data(c_3po, PERSON_KEYS)
    evac_transport['passenger_manifest'].append(leia)
    evac_transport['passenger_manifest'].append(c_3po)
    # copy-creat escorts
    evac_transport['escorts'] = []
    #freighter1
    luke_x_wing = starfighters.copy()
    luke = get_swapi_resource('https://swapi.co/api/people/', {'search': 'Luke Skywalker'})['results'][0]
    luke = clean_data(luke)
    luke = filter_data(luke, PERSON_KEYS)
    r2_d2 = get_swapi_resource('https://swapi.co/api/people/', {'search': 'R2-D2'})['results'][0]
    r2_d2 = clean_data(r2_d2)
    r2_d2 = filter_data(r2_d2, PERSON_KEYS)
    luke_x_wing = assign_crew(luke_x_wing, {'pilot': luke, 'astromech_droid': r2_d2})
    evac_transport['escorts'].append(luke_x_wing)
    #flighter2
    wedge_x_wing = starfighters.copy()
    wedge = get_swapi_resource('https://swapi.co/api/people/', {'search': 'Wedge Antilles'})['results'][0]
    wedge = clean_data(wedge)
    wedge = filter_data(wedge, PERSON_KEYS)
    r5_d4 = get_swapi_resource('https://swapi.co/api/people/', {'search': 'R5-D4'})['results'][0]
    r5_d4 = clean_data(r5_d4)
    r5_d4 = filter_data(r5_d4, PERSON_KEYS)
    wedge_x_wing = assign_crew(wedge_x_wing, {'pilot': wedge, 'astromech_droid': r5_d4})
    evac_transport['escorts'].append(wedge_x_wing)
    # update evac 
    evac_plan['transport_assignments'] = [evac_transport]
    echo_base['evacuation_plan'] = evac_plan
    # write json
    write_json('swapi_echo_base-v1p1.json', echo_base)

if __name__ == '__main__':
    main()