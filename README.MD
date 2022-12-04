# Plane Notifier

Automate <a href="https://www.flightradar24.com">Flightradar24</a> plane spotting with python by receiving a windows notification when a plane is about to fly over your area (only for personal use)

![Flight noti](./images/notiexample.jpg?raw=false)

## Installation

```console
git clone https://github.com/ravenstx/PlaneNotifier.git
```

## Setup / Usage

_install the requirements_

```
cd PlaneNotifier
python -m pip install -r requirements.txt
```

_next go into the file called planenotifier.py and put your latitude and longitude_
_for this example I took the coordinates from the Eiffel Tower_

```
config = {
    'lat': 48.8585,
    'long': 2.2942,
    'km_diameter': 25,
    'visible_km_radius': 3.5
}
```

_run planenotifier.py_ <br>

```
python planenotifier.py
```

(This is what happens under the hood, when a plane's predicted path is in youre radius you will receive a notification)

![demo](./images/demo.png?raw=false)
