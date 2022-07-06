# Want to scrape music tour location data from site; (Maybe) Use 'requests' to save html file (or whatever it is)
## (done) Use RegEx to isolate location data
### (done) Write location data to spreadsheet/csv - (used xlsxwriter for .xlsx file)
#### (done) Upload spreadsheet of location data to Google Maps to create custom map of tour venue locations

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import csv
from pprint import pprint
import googlemaps # pip install googlemaps
from googlemaps import convert
import pandas as pd
import folium
from folium.plugins import MarkerCluster




API_KEY = 'AIzaSyCVyjJrpSv4-tb2OKAMxLhJb6PArjE0NUs' #should store in separate file

map_client = googlemaps.Client(API_KEY)

# geocode functions
def geocode(client, address=None, place_id=None, components=None, bounds=None, region=None,
            language=None):
    """
    Geocoding is the process of converting addresses
    (like ``"1600 Amphitheatre Parkway, Mountain View, CA"``) into geographic
    coordinates (like latitude 37.423021 and longitude -122.083739), which you
    can use to place markers or position the map.

    :param address: The address to geocode.
    :type address: string

    :param place_id: A textual identifier that uniquely identifies a place,
        returned from a Places search.
    :type place_id: string

    :param components: A component filter for which you wish to obtain a
        geocode, for example: ``{'administrative_area': 'TX','country': 'US'}``
    :type components: dict

    :param bounds: The bounding box of the viewport within which to bias geocode
        results more prominently.
    :type bounds: string or dict with northeast and southwest keys.

    :param region: The region code, specified as a ccTLD ("top-level domain")
        two-character value.
    :type region: string

    :param language: The language in which to return results.
    :type language: string

    :rtype: list of geocoding results.
    """

    params = {}

    if address:
        params["address"] = address

    if place_id:
        params["place_id"] = place_id

    if components:
        params["components"] = convert.components(components)

    if bounds:
        params["bounds"] = convert.bounds(bounds)

    if region:
        params["region"] = region

    if language:
        params["language"] = language

    return client._request("/maps/api/geocode/json", params).get("results", [])


def reverse_geocode(client, latlng, result_type=None, location_type=None,
                    language=None):
    """
    Reverse geocoding is the process of converting geographic coordinates into a
    human-readable address.

    :param latlng: The latitude/longitude value or place_id for which you wish
        to obtain the closest, human-readable address.
    :type latlng: string, dict, list, or tuple

    :param result_type: One or more address types to restrict results to.
    :type result_type: string or list of strings

    :param location_type: One or more location types to restrict results to.
    :type location_type: list of strings

    :param language: The language in which to return results.
    :type language: string

    :rtype: list of reverse geocoding results.
    """

    # Check if latlng param is a place_id string.
    #  place_id strings do not contain commas; latlng strings do.
    if convert.is_string(latlng) and ',' not in latlng:
        params = {"place_id": latlng}
    else:
        params = {"latlng": convert.latlng(latlng)}

    if result_type:
        params["result_type"] = convert.join_list("|", result_type)

    if location_type:
        params["location_type"] = convert.join_list("|", location_type)

    if language:
        params["language"] = language

    return client._request("/maps/api/geocode/json", params).get("results", [])





url = 'https://manchesterorchestra.com/'

driver = webdriver.Chrome(r'C:\Users\garph\OneDrive\Documents\coding projects\test_manchester\chromedriver.exe')
driver.get(url)
sleep(3)
page = driver.page_source # html source
soup = BS(page, 'lxml') # beautify [soup] it

#print('soup:', soup)

#content_dates = soup.find('ul', class_=r'seated-event-date-cell')
#print('content_dates:', content_dates)
dates = soup.find_all('div', class_=r'seated-event-date-cell')
print(dates)

locations = soup.find_all('div', class_=r'seated-event-venue-location')
print(locations)


# write to csv
with open(r'C:\Users\garph\OneDrive\Documents\coding projects\test_manchester\ManTourLoc.csv', mode='w', newline='') as f:
    ManLocCSV = csv.writer(f, delimiter=',')
    ManLocCSV.writerow(['date','location', 'lat','lng'])



    for i, j in enumerate(dates):
        date = dates[i].text.strip()
        location = locations[i].text.strip()

        response = map_client.geocode(location)

        lat = response[0]['geometry']['location']['lat']
        lng = response[0]['geometry']['location']['lng']

        print(date, location)
        ManLocCSV.writerow([date, location, lat, lng])

driver.close()

# create map
m = folium.Map(tiles = 'OpenStreetMap', zoom_start = 10) # zoom_start doesn't do anything if [map] location is default

df = pd.read_csv(r'C:\Users\garph\OneDrive\Documents\coding projects\test_manchester\ManTourLoc.csv')

markerCluster = MarkerCluster().add_to(m)

for i, row in df.iterrows():
    lat = df.at[i, 'lat']
    lng = df.at[i, 'lng']
    loc = df.at[i, 'location']
    date = df.at[i, 'date']
    tooltip = loc
    popup = date +' <br> '+ loc

    folium.Marker(location=[lat, lng], popup = popup, tooltip=tooltip, icon = folium.Icon(color = 'blue')).add_to(markerCluster)


#folium.Marker(location = [48.86762, 2.3624], popup = 'testing', icon = folium.Icon(color = 'blue')).add_to(m)
#folium.Marker(location = [49.86762, 1.3624], popup = 'TEXT', icon = folium.Icon(color = 'red')).add_to(m)

m.save(r'C:\Users\garph\OneDrive\Documents\coding projects\test_manchester\index.html')
