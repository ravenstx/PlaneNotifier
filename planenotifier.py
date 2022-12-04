import time
from flightdetector import Flightdetector
from flight import Flight

# fill this in before use
config = {
    'lat': 48.8585,
    'long': 2.2942,
    # the diameter of the area around your coordinates you want to look for flights every 5 seconds (25 should be good)
    'km_diameter': 25,
    # if a planes path is predicted to fly in this radius than you will get a notification (3-4 should be good)
    'visible_km_radius': 3.5
}

# list to add and delete flight objects
flights_list = []


def main(flightscanner):

    flightscanner.print_bounds()
    flights = flightscanner.get_flights()

    flights_amount = len(flights.keys())
    print(f"{flights_amount} flights detected")

    count = 0
    for key, value in flights.items():
        count += 1
        print(f"\t{count}. {key} | {value}")

        # only add flight object if the flight object is not in the list
        is_key_in_list = False
        for flight in flights_list:
            if flight.id == key:
                is_key_in_list = True

        if is_key_in_list is not True:
            new_flight = Flight(key, value)
            flights_list.append(new_flight)

    # delete the flight objects that are not being detected anymore
    # flights_list.copy() and flights_list[:] work the same
    for flight in flights_list.copy():
        if flight.id not in flights.keys():
            #print(f"{flight.id} not visible anymore")
            flights_list.remove(flight)

    print("\n")

    for flight in flights_list:

        flight.predict_flight_track(
            flightscanner.lat, flightscanner.long, flightscanner.visible_km_radius)

    # print(flights_list)

    # keep this on 5 to 10 seconds to
    time.sleep(5)


if __name__ == '__main__':
    try:

        flightscanner = Flightdetector(
            config["lat"], config["long"], config["km_diameter"], config["visible_km_radius"])
        while True:

            main(flightscanner)

    except KeyboardInterrupt:
        print("program has stopped")
