# Author: Colleen Lemak
# File: moisture-notifs.py
# Objective: Send data from RaspberryPi's D0 pin to monitored AWS topic 

import RPi.GPIO as GPIO
import time
import json
from config import TOPIC, CLIENT, ENDPOINT, ROOT_CA_PATH, PRIVATE_KEY_PATH, CERT_PATH
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Configure client information
client = AWSIoTMQTTClient(CLIENT)
client.configureEndpoint(ENDPOINT, 8883)
client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERT_PATH)

# Connect to AWS IoT
client.connect()
print("Connected to AWS!")
	
# Publish results to AWS
def send_moisture_notif(is_dry):
    # Publish results
    payload = json.dumps({"moisture": "dry" if is_dry else "wet"})
    client.publish(TOPIC, payload, 1)
    print(f"Published: {payload}")
    # Print to console
    if is_dry:
        print("Soil is dry!")
    else:
        print("Soil moisture is adequate")

# Set up GPIO
GPIO.setmode(GPIO.BCM)
D0_PIN = 17
GPIO.setup(D0_PIN, GPIO.IN)

try:
    interval_seconds = 14400 # check levels every 4 hours
    while True:
        # Read and send sensor data
        is_dry = (GPIO.input(D0_PIN) == GPIO.LOW)
        print(f"Sensor reading: {'dry' if is_dry else 'wet'}")
        send_moisture_notif(is_dry)
        time.sleep(interval_seconds)
        print("Measuring moisture levels...")
        
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    client.disconnect()
    print("Disconnected from AWS.")
