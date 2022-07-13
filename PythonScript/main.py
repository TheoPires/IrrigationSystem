import network
from time import sleep

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("raspi-webgui", "ChangeMe")
if station.isconnected() == True:
    print('WIFI Connection Succeed')

SERVER = '10.3.141.1'
CLIENT_ID = 'ESP32'
TOPIC = 'test'
from umqtt.simple import MQTTClient
client = MQTTClient(CLIENT_ID, SERVER)
sleep(5)
if client.connect() == 0:
    print('MQTT Connection Succeed')

while True:
    client.publish(TOPIC, 'test_main')
    sleep(4)
client.publish(TOPIC, 'test_main')
