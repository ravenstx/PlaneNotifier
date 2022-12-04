import calculations
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}


class Flightdetector:

    def __init__(self, lat, long, km_diameter=25, visible_km_radius=3):
        self.lat = lat
        self.long = long

        self.bounds = calculations.get_bounds(
            self.lat, self.long, km_diameter)
        self.visible_km_radius = visible_km_radius

    def get_flights(self):
        try:
            response = requests.get(
                "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?faa=1&bounds={}%2C{}%2C{}%2C{}".format(self.bounds['lat_max'], self.bounds['lat_min'], self.bounds['long_min'], self.bounds['long_max']), headers=headers, timeout=2)
        except requests.exceptions.SSLError:
            pass
        if response.status_code != 200:
            return {}
        response_dict = response.json()
        # delete the 2 non-flight keys of the dict
        del response_dict['full_count']
        del response_dict['version']

        return response_dict

    def print_bounds(self):
        print("{} | {} | {} | {}".format(
            self.bounds['lat_max'], self.bounds['lat_min'], self.bounds['long_min'], self.bounds['long_max']))
