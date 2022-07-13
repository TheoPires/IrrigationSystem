import time
from network import WLAN
from umqtt.simple import MQTTClient
from ubinascii import hexlify
import sys

CLIENT_ID = "demo-pub"

#IP du Raspberry PI, il faut sans doute changer l'ip
MQTT_SERVER = "10.3.141.1"

MQTT_USER = 'pires'
MQTT_PSWD = 'pires'

print("Création MQTTClient")
q = MQTTClient(client_id = CLIENT_ID, server = MQTT_SERVER, user = MQTT_USER, password = MQTT_PSWD)

if q.connect != 0:
    print("Erreur connexion")
    sys.exit()

print("Connecter")

# connexion objet
sMac = hexlify(WLAN().config('mac')).decode()
q.publish("connect/%s" % CLIENT_ID, sMac)

for i in range(10):
    print("pub %s" % i)
    q.publish("demo/compteur", str(i))
    time.sleep(1)

q.disconnect()
print("Fin de traitement")
