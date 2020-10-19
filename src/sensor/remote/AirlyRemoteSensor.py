import datetime
import json
import urllib.request

import src.sensor.RemoteSensor as RemoteSensor


class AirlyRemoteSensor(RemoteSensor):
    api_key = '7eXz1k8alkGdr1KzCBy7r01J7AkqFkxB'
    url = 'https://airapi.airly.eu/v2/measurements/installation?indexType=AIRLY_CAQI&installationId=3493'
    data = None

    def fetch_data(self) -> None:
        req = urllib.request.Request(self.url, headers={"apikey": self.api_key})
        with urllib.request.urlopen(req) as response:
            self.data = json.loads(response.read().decode())

    def get_data(self) -> list:
        if self.data is None:
            self.fetch_data()
        return self.data

    def is_stale(self) -> bool:
        data_timestamp = datetime.datetime.fromtimestamp(self.data.current.tillDateTime)
        check_timestamp = datetime.datetime.now()-datetime.timedelta(minutes=18)
