from requests_oauthlib import OAuth1
from bs4 import BeautifulSoup as bs
import requests
import json
import secrets # file that contains your API key

API_KEY = secrets.API_KEY
API_SECRET = secrets.API_SECRET

oauth = OAuth1(API_KEY,API_SECRET)

class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category, name, address, zipcode, phone):
        self.category = category if category else ""
        self.name = name if name else "no name"
        self.address = address if address else "no address"
        self.zipcode = zipcode if zipcode else "no zipcode"
        self.phone = phone if phone else "no phone"

    def info(self):
        return "{} ({}): {} {}".format(self.name, self.category, self.address, self.zipcode)


def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
    '''
    URL = 'https://www.nps.gov'
    response = requests.get(URL)
    sp = bs(response.text, 'html.parser')

    div = sp.find('div', class_="SearchBar-keywordSearch input-group input-group-lg")
    ul = div.find('ul', class_="dropdown-menu SearchBar-keywordSearch")
    lis = []
    for i in ul.findAll('li'):
        if i.find('ul'):
            break
        lis.append(i)

    dict = {}
    for i in lis:
        url = i.a['href']
        dict[i.text.lower()] = URL + url
    return dict
#print(len(build_state_url_dict()))


def get_site_instance(site_url):
    '''Make instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''
    response = requests.get(site_url)
    sp = bs(response.text, 'html.parser')

    category = sp.find('span', {'class': "Hero-designation"}).text.strip()
    name = sp.find('a', {'class': 'Hero-title'}).text.strip() #.string the same
    city = sp.find('span', {'itemprop': 'addressLocality'}).text.strip() #cannot use itemprop_='', but class_=
    state = sp.find('span', {'class': 'region'}).text.strip()
    address = city + ", " + state
    zipcode = sp.find('span', {'class': 'postal-code'}).text.strip()
    phone = sp.find('span', {'itemprop': 'telephone'}).text.strip()
    return NationalSite(category, name, address, zipcode, phone)
#print(get_site_instance("https://www.nps.gov/isro/index.htm"))


def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''
    URL = 'https://www.nps.gov'
    response = requests.get(state_url)
    sp = bs(response.text, 'html.parser')

    lis_h3 = sp.find('div', {'id': 'parkListResultsArea'}).findAll('h3')
    site_url_lis = []
    for i in lis_h3:
        site = i.a['href']
        site_url_lis.append(site)

    instance_lis = []
    for url in site_url_lis:
        url = URL + url
        instance_lis.append(get_site_instance(url))
    return instance_lis
#print(get_sites_for_state("https://www.nps.gov/state/mi/"))

def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.

    Parameters
    ----------
    site_object: object
        an instance of a national site

    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    params={'key':API_KEY,
            'origin':site_object.zipcode,
            'radius':10,'maxMatches':10,
            'ambiguities':'ignore',
            'outFormat':'json'}
    response = requests.get('http://www.mapquestapi.com/search/v2/radius',params=params,auth=oauth).json()
    return response
#print(get_nearby_places(get_site_instance('https://www.nps.gov/slbe/index.htm')))


class Nearby:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a nearby site (e.g. 'National Park', '')
        some sites have blank category.

    name: string
        the name of a nearby site (e.g. 'Isle Royale')

    address: string
        the street address of a nearby site (e.g. '1701 Memorial Rd')

    city: string
        the city of a national site (e.g. 'Houghton')
    '''
    def __init__(self, category, name, address, city):
        self.category = category if category else "no category"
        self.name = name if name else "no name"
        self.address = address if address else "no address"
        self.city = city if city else "no city"

    def info(self):
        return "{} ({}): {}, {}".format(self.name, self.category, self.address, self.city)


if __name__ == "__main__":
    state_dict = build_state_url_dict()
    search = input(" Enter a state name, e.g. Michigan/michigan/MICHIGAN: ")
    while True:
        if search.lower() == 'exit':
            break
        else:
            while True:
                if search.lower() in state_dict.keys():
                    state_url = state_dict[search.lower()]
                    sites = get_sites_for_state(state_url)
                    if len(sites) != 0:
                        print(' -----------------------------------\n '
                              'List of Natinoal Sites in' + search +
                              ':\n -----------------------------------')
                        for i in range(len(sites)):
                            print(" [{}] {}".format(i + 1, sites[i].info()))
                        search = input(" Enter an index number to view details, or 'back', or 'exit': ")
                        while True:
                            if search.lower() in ('back','exit'):
                                break
                            elif search.isnumeric() and int(search) <= len(sites):
                                num = int(search) - 1
                                nearby = get_nearby_places(sites[num])
                                for place in nearby['searchResults']:
                                    category = place['fields']['group_sic_code_name']
                                    name = place['name']
                                    address = place['fields']['address']
                                    city = place['fields']['city']
                                    place_instances = Nearby(category, name, address, city)
                                    print(" - {}".format(place_instances.info()))
                                search = input(" Enter an index number to view details, or 'back', or 'exit': ")
                            else:
                                print(" [Error]: invalid input")
                                search = input(" Enter an index number to view details, or 'back', or 'exit': ")
                        break
                    else:
                        print(" No sites found.")
                        break
                else:
                    print(" [Error]: invalid input")
                    break
            if search.lower() != 'exit':
                search = input(" Enter a state name, e.g. Michigan/michigan/MICHIGAN: ")
            else:
                break

    print(' Thanks for using the service, bye!')