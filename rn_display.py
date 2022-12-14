import paho.mqtt.client as mqtt
import pandas as pd
import io
import pickle
import configparser

#This app subscribes to the statistics calculated by 'rn_processor.py' and prints them in tabular layout

config = configparser.ConfigParser()
config.read('config.ini')

PROCESSED_TOPIC_NAME = config['DEFAULT']["PROCESSED_TOPIC_NAME"]
BROKER_HOSTNAME = config["DEFAULT"]["BROKER_HOSTNAME"]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(PROCESSED_TOPIC_NAME)

def on_message(client, userdata, msg):
    msg_obj = pickle.load(io.BytesIO(msg.payload))
    print("NEW DATA RECEIVED")
    print("\n1 minute averages")
    print(msg_obj["1_min"].to_markdown())
    print("\n5 minute averages")
    print(msg_obj["5_min"].to_markdown())
    print("\n30 minute averages")
    print(msg_obj["30_min"].to_markdown())

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER_HOSTNAME, 1883, 60)
    except:
        pass
    client.loop_forever()