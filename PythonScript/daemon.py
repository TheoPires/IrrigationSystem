#daemon présent sur le rapsberry
#check la bdd pour voir les activations et desactivations
#à communiquer aux vannes
from time import sleep, strftime
from datetime import datetime
from dateutil.parser import parse
import requests, json
import syslog
import sys
import paho.mqtt.client as mqtt

API = "https://smart-irrigation-uiv-rouen.herokuapp.com/"

syslog.syslog('Daemon start')

# Informations MQTT Server
MQTT_SERVER = "10.3.141.1"
CLIENT_ID = 'RASPBERRY_PI'
TOPIC = 'test'

client = mqtt.Client(CLIENT_ID)
if client.connect(MQTT_SERVER) == 0:
    print('MQTT Connection Succeed')
    syslog.syslog('MQTT Connection Succeed')

while True:
    r = requests.get(API + 'gestVannes/listVanne')
    listVannes = json.loads(r.text)

    currentTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    currentTime = parse(currentTime)


    syslog.syslog('Checking status of system')
    for vanne in listVannes:
        idVanne = vanne["id"]
        nameVanne = vanne["nomNoeud"]
        if vanne["start"] is not None or vanne["end"] is not None:
            startTime = parse(vanne["start"])
            endTime = parse(vanne["end"])
            print('idVanne : ' + str(idVanne))
            print('startTime : ' + str(startTime))
            print('endTime : ' + str(endTime))
            print('currentTime : ' + str(currentTime))
            print('Vanne status : ' + str(vanne['status']))
            url = API+"gestVannes/vanne/"
            if startTime < currentTime and not vanne["status"] and endTime > currentTime:
                syslog.syslog('Activating ' + nameVanne)
                #message ESP32
                client.publish(TOPIC, vanne["nomNoeud"] + '#ON');
                #requete put
                data = {"id": idVanne, "nomNoeud": nameVanne, "status": True}
                respo = requests.put(url+str(idVanne), data)
                print("activation")

            if endTime < currentTime and vanne["status"]:
                syslog.syslog('Desactivating ' + nameVanne)
                #message ESP32
                client.publish(TOPIC, vanne["nomNoeud"] + '#OFF');
                #requete put
                data = {"id": idVanne, "nomNoeud": nameVanne, "status": False}
                respo = requests.put(url+str(idVanne), data)
                print("desactivation")
        else:
            print("Aucune date pour la vanne [" + str(idVanne) + "] : " + nameVanne + ".")
            syslog.syslog(syslog.LOG_INFO, 'No date found')
    print("******** attente 1 scd *********")
    sleep(1)
