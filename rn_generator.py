import paho.mqtt.publish as publish
import random
import time
import datetime
import json
import configparser

#This file generates random numbers at random time intervals and publishes them to mqtt broker

config = configparser.ConfigParser()
config.read('config.ini')

TOPIC_NAME = config['DEFAULT']["TOPIC_NAME"]
BROKER_HOSTNAME = config["DEFAULT"]["BROKER_HOSTNAME"]


def loop():
    time.sleep(random.random()*29+1) #Sleep between 1 and 30 seconds
    rand_num = random.randint(1,100)
    message_obj = {"rand_num":rand_num, "timestamp":datetime.datetime.now().isoformat()}
    message = json.dumps(message_obj)
    publish.single(TOPIC_NAME,message,hostname=BROKER_HOSTNAME)
    print("Published message",message)
    loop()

if __name__=="__main__":
    loop()