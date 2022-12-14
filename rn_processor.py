import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import pandas as pd
import json
import datetime
import pickle
import io
import configparser

#This file takes incoming random numbers from MQTT broker, stores them, 
#resamples and averages the data and publishes back to the broker on a different
#topic

config = configparser.ConfigParser()
config.read('config.ini')

BROKER_HOSTNAME = config["DEFAULT"]["BROKER_HOSTNAME"]
RAW_TOPIC_NAME = config["DEFAULT"]["TOPIC_NAME"]
PROCESSED_TOPIC_NAME = config["DEFAULT"]["PROCESSED_TOPIC_NAME"]
PROCESSED_MAX_LENGTH = int(config["DEFAULT"]["PROCESSED_MAX_LENGTH"]) #Max entries in processed data timeseries sent to broker

#Data is persisted as a local file. In prod would need to consider using a proper 
#database or at least limiting its file size (e.g. by pruning old data)
DATA_FILENAME = config["DEFAULT"]["DATA_FILENAME"]

try:
    df = pd.read_pickle(DATA_FILENAME)
except:
    print("No stored data found, creating new data file at",DATA_FILENAME)
    df = pd.DataFrame(columns=["rand_num"],index=pd.Index([],dtype='datetime64[ns]'))
    df.to_pickle(DATA_FILENAME)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(RAW_TOPIC_NAME)

def on_message(client, userdata, msg):
    global df
    msg_obj = json.loads(msg.payload)
    timestamp = datetime.datetime.fromisoformat(msg_obj["timestamp"])
    value = int(msg_obj["rand_num"])

    df.loc[timestamp] = value

    df.to_pickle(DATA_FILENAME)
    
    #Create averages
    avg_1min = df.resample('T').mean().iloc[-PROCESSED_MAX_LENGTH:]
    avg_5min = df.resample('5T').mean().iloc[-PROCESSED_MAX_LENGTH:]
    avg_30min = df.resample('30T').mean().iloc[-PROCESSED_MAX_LENGTH:]

    processed_obj = {
        '1_min':avg_1min,
        '5_min':avg_5min,
        '30_min':avg_30min
    }

    with io.BytesIO() as f:
        pickle.dump(processed_obj,f)
        f.seek(0)
        publish.single(PROCESSED_TOPIC_NAME,f.read(),hostname=BROKER_HOSTNAME)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOSTNAME, 1883, 60)

    client.loop_forever()