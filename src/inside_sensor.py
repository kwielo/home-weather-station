from signal import signal, SIGINT
from sys import exit
import psycopg2
import airly
from getkey import getkey, keys
import write_on_display
import bme280
import smbus2
import datetime
from time import sleep


conn = psycopg2.connect(
            host="localhost",
            database="weather_station",
            user="dev",
            password="d3v")

insert_measure_sql = """
    insert into measure (temperature, pressure, humidity, outside_temp, pm_2_5, pm_10, caqi, meter_id) 
    values (%s, %s, %s, %s, %s, %s, %s, %s) 
    returning id
    """

airly_last_read = datetime.datetime.now()-datetime.timedelta(minutes=30)
caqi = 0

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)

write_on_display.write('Initiating\nsystems...')
sleep(1)


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    write_on_display.clear()
    f.close()
    conn.close()
    exit(0)


if __name__ == '__main__':
    signal(SIGINT, handler)


while True:
    if airly_last_read < datetime.datetime.now()-datetime.timedelta(minutes=20):
        airlyData = airly.getData()
        caqiRaw = airlyData["current"]["indexes"][0]["value"]
        caqi = round(caqiRaw)
        outside_temp = airlyData["current"]["values"][5]["value"]
        pm_2_5 = airlyData["current"]["values"][1]["value"]
        pm_10 = airlyData["current"]["values"][2]["value"]
        airly_last_read = datetime.datetime.now()

    bme280_data = bme280.sample(bus, address)
    humidity = round(bme280_data.humidity)
    humidity2 = bme280_data.humidity
    pressure = round(bme280_data.pressure)
    pressure2 = bme280_data.pressure
    temperature = round(bme280_data.temperature)
    temperature2 = bme280_data.temperature
    msg = f'H:{humidity}% {temperature}\u00b0C\nhPa:{pressure}\nCAQI:{caqi} {outside_temp}\u00b0C'
    write_on_display.write(msg)
    time = datetime.datetime.now()
    f = open("weather.log", "a")
    f.write(f'{time};{humidity2};{pressure2};{temperature2};{caqiRaw};{outside_temp};{pm_2_5};{pm_10}\n')

    cur = conn.cursor()
    cur.execute(insert_measure_sql, (temperature2, pressure2, humidity2, outside_temp, pm_2_5, pm_10, caqiRaw, 2))
    conn.commit()
    cur.close()

    f.close()
    sleep(60*5)


