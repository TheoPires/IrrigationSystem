from dht import DHT11
from machine import Pin
from time import sleep

sensor = DHT11(Pin(15, Pin.IN, Pin.PULL_UP))

while True:
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        print("Temperature : ")
        print(t)
        print("Humidity : ")
        print(h)
    except OSError:
        print('Failed to read sensor.')
    sleep(4)
