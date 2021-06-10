import json
import threading
import datetime
import subprocess

INTERVAL = 15*60

def get_current_speed_data():
    speed_data = subprocess.run(['speedtest', '-f', 'json'], capture_output=True).stdout
    return json.loads(speed_data)


def convert_to_mbps(bytes_):
    return (bytes_ * 8) / 1000000


def update_speed_data(speed_data):
    now = datetime.datetime.now()
    while len(speed_data[0]['x']) and now - datetime.datetime.fromisoformat(speed_data[0]['x'][0]) > datetime.timedelta(days=7):
        speed_data[0]['x'].pop()
        speed_data[0]['y'].pop()
        speed_data[1]['x'].pop()
        speed_data[1]['y'].pop()

    speedtest_results = get_current_speed_data()
    speed_data[0]['x'].append(datetime.datetime.now().isoformat())
    speed_data[0]['y'].append(convert_to_mbps(speedtest_results['download']['bandwidth']))
    speed_data[1]['x'].append(datetime.datetime.now().isoformat())
    speed_data[1]['y'].append(convert_to_mbps(speedtest_results['upload']['bandwidth']))

    return speed_data

def update_json_file():
    with open('speed_data.json', 'r+') as json_file:
        contents = json.load(json_file)

        contents = update_speed_data(contents)

        json_file.seek(0)
        json_file.truncate()
        json.dump(contents, json_file)

def start_maintence():
    def wrapper():
        start_maintence()
        update_json_file()

    timer = threading.Timer(INTERVAL, wrapper)
    timer.start()
