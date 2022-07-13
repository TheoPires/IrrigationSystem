from machine import Pin
import network
from simple import MQTTClient
from time import sleep
import json

##########################
#   Configuration WIFI   #
##########################
WIFI_SSID = 'raspi-webgui'
WIFI_PASSWD = 'ChangeMe'

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)


wifi = network.WLAN(network.STA_IF)
wifi.active(True)
if wifi.connect(WIFI_SSID, WIFI_PASSWD) == 0:
    print('WIFI Connection Succeed')

##########################
# FIN Configuration WIFI #
##########################


# Informations MQTT Server
MQTT_SERVER = "10.3.141.1"
CLIENT_ID = 'ESP32_1'
TOPIC = 'test'

con = MQTTClient(CLIENT_ID, MQTT_SERVER)
sleep(5)
if con.connect() == 0:
    print('MQTT Connection Succeed')



##########################
#   JSON FILE            #
##########################

f = open('esp.json')
dictionnary = json.load(f)
f.close()

##########################
#   FIN JSON FILE        #
##########################


"""
La fonction mqtt_callback est appelée à chaque fois qu'un message est publié
dans un topic auquel on est abonnée
"""
def mqtt_callback(topic, msg):
    print("message reçu : ", msg.decode())
    print("topic : ", topic.decode())
    
    sms_parse = msg.decode().split('#')
    
    pinNumber = dictionnary[sms_parse[0]]
    led = Pin(pinNumber, Pin.OUT)
    
    if sms_parse[1] == 'ON':
        led.value(0)
        print('Activation LED ' + sms_parse[0])
    else:
        led.value(1)
        print('Desactivation LED ' + sms_parse[0])

#Définition de la fonction qui reçoit les messages
con.set_callback(mqtt_callback)

#Abonnement au Topic
con.subscribe(TOPIC)

print('En attente de message sur le topic')
while True:
    con.wait_msg()
    #con.wait_msg() "wait_msg" est bloquant contrairement à "check_msg"
