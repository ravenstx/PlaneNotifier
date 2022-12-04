import requests
from winotify import Notification, audio
import calculations
import os

headers = {
    'accept': 'application/json'
}


class Flight:

    def __init__(self, flight_id, details):

        self.id = str(flight_id)
        # self.icao_24bit = details[0]
        self.latitude = details[1]
        self.longitude = details[2]
        self.heading = details[3]
        self.altitude = details[4]
        self.ground_speed = details[5]
        self.aircraft_code = details[8]
        self.origin_airport_iata = details[11]
        self.destination_airport_iata = details[12]
        self.callsign = details[16]
        self.notification_sended = False

    def get_aircraft_model(self):
        # send get request and stop waiting for the response after 2 seconds and return 'N/A' else handle the response data
        try:
            response = requests.get(
                f"https://data-live.flightradar24.com/clickhandler/?version=1.5&flight={self.id}", headers=headers, timeout=2)
        except requests.exceptions.Timeout as err:
            print(err)
            return 'N/A'
        # check if response is a status code 200
        if response.status_code != 200:
            return 'N/A'
        response_dict = response.json()
        # if there is no aircraft model name pass 'N/A'
        try:
            model = response_dict['aircraft']['model']['text']
            if model == '' or model is None:
                return 'N/A'
            else:
                return model

        except KeyError:
            return 'N/A'

    def predict_flight_track(self, lat, long, kmradius):
        prediction = calculations.calculate_flyby(
            self.heading, self.latitude, self.longitude, lat, long)

        distance_user_to_prediction = calculations.get_distance_from_lat_lon_in_km(
            prediction['lat'], prediction['long'], lat, long)

        if distance_user_to_prediction < kmradius:
            self.print_notification()

    def get_link(self):
        return f"https://www.flightradar24.com/{self.callsign}/{self.id}"

    def __str__(self) -> str:
        return f"| {self.id} |"

    def __repr__(self) -> str:
        return self.id

    def print_notification(self):
        if self.notification_sended == False:
            self.notification_sended = True  # set notif
            aircraft_model = self.get_aircraft_model()
            path_to_icon = r'{}\images\notificationicon.png'.format(
                os.getcwd())
            noti = Notification(app_id="Flight noti",
                                title=f"Flight heading {calculations.angle_to_compass(self.heading)}",
                                msg=f"{aircraft_model} \naltitude: {calculations.feet_to_meter(self.altitude)} meter",
                                duration="long",
                                icon=path_to_icon)
            noti.add_actions(label="link to plane", launch=self.get_link())
            noti.show()
