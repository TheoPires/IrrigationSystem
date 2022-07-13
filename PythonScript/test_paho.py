import paho.mqtt.client as mqtt

# Informations MQTT Server
MQTT_SERVER = "10.3.141.1"
CLIENT_ID = 'RASPBERRY_PI'
TOPIC = 'test'

client = mqtt.Client(CLIENT_ID)

if client.connect(MQTT_SERVER) == 0:
	print('MQTT Connection Succeed')

client.publish(TOPIC, 'coucou')

