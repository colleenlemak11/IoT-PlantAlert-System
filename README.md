# Soil Moisture Monitoring with AWS IoT and RaspberryPi

## Project Overview
The objective of this project is to automate email-notification reminders to water your house plant using AWS. This project creates an IoT system using a RaspberryPi 3 and a YL-69 soil moisture sensor to monitor soil moisture levels in real-time. The system sends readings to AWS IoT Core and AWS Lambda then processes the data and triggers an Amazon SNS email alert if the soil is considered dry.

## Technology Used
- Raspberry Pi 3 (with Python)
- YL-69 Soil Moisture Sensor
- AWS IoT Core (for device connection and MQTT messaging)
- AWS Lambda (for serverless processing)
- Amazon SNS (for email notifications)
- AWS IoT SDK (for MQTT communication)
- Python (for GPIO reading and AWS SDK)

## How It Works
### Soil Moisture Monitoring:
- A YL-69 soil moisture sensor is connected to the Raspberry Pi GPIO pins. It provides readings indicating the moisture level of the soil (either "dry" or "wet").
- The sensor output is read via Python code using GPIO pins, with the moisture value being published to an MQTT topic on AWS IoT Core.

### AWS IoT Core:
- The Raspberry Pi securely connects to AWS IoT Core using an MQTT client and publishes moisture readings to the topic moistureSensor.
- The connection to AWS IoT Core is secured using certificates.

### Lambda Function:
- AWS Lambda is triggered by the MQTT message published to the moistureSensor topic.
- The Lambda function checks the moisture data and determines if the soil is too dry or considered adequate.

### Email Notification:
- If the moisture level is too low (soil is dry), the Lambda function sends a message to an SNS topic, which sends an email notification to the subscribed recipient.

## Hardware Setup
1. **Raspberry Pi 3**: Configured to read from GPIO pins and connect to AWS IoT Core.
2. **YL-69 Soil Moisture Sensor**: Measures the moisture level in the soil. This sensor is connected to the Raspberry Pi GPIO pins for moisture detection.
3. **Jumper Wires**: For connecting the Raspberry Pi GPIO pins to the YL-69 sensor on the breadboard.
4. **Power Supply**: For powering both the Raspberry Pi and the YL-69 sensor (3.3-5V).

### Wiring the YL-69 Sensor to the Raspberry Pi:
1. **Connect VCC (5V) Pin** from the YL-69 sensor to the **5V** pin on the Raspberry Pi.
2. **Connect GND (Ground) Pin** from the YL-69 sensor to the **GND** pin on the Raspberry Pi.
3. **Connect the D0 Pin** (digital output) from the YL-69 sensor to the **GPIO17** pin on the Raspberry Pi for moisture detection.

*The digital pin (D0) on the YL-69 sensor provides a HIGH or LOW signal based on the moisture level. When the soil is dry, my sensor sends a LOW signal; when it's wet, the sensor sends a HIGH signal.*

## 1. Software Setup
### RaspberryPi Configuration
- **Install necessary libraries**:
     - Install `RPi.GPIO` for GPIO control.
     - Install the AWS IoT SDK: `pip install AWSIoTPythonSDK`
   
   - **Configure AWS IoT Certificates**:
     - Register your Raspberry Pi as a thing in **AWS IoT Core**.
     - Download the X.509 certificates (CA certificate, private key, and device certificate) and store them on the Raspberry Pi.
     - Set up your **IoT policy** to allow device communication (connect, publish, etc.).

   - **Python Script**:
     - Write a Python script to read the sensor data and publish it to the AWS IoT MQTT topic `moistureSensor`.
     - The script includes code to publish messages to AWS IoT Core, check the moisture level, and handle the GPIO input.

### 2. AWS Setup
   - **AWS IoT Core**:
     - Create a new thing in the **AWS IoT Core Console** and download the device certificates.
     - Set up an IoT policy that allows publishing to the `moistureSensor` topic.
   - **Create Rule to Trigger Lambda Function**
   - Create a Rule to `SELECT * FROM 'moistureSensorTopic'` and trigger the Lambda function.
      - For the **Action** of the rule, choose **Invoke AWS Lambda function** and select your Lambda function that will process the moisture data and send the email alert.
   - **AWS Lambda**:
     - Write and deploy a Lambda function that processes the data and sends email notifications via SNS.
     - Ensure the Lambda function has the necessary permissions to access SNS.

   - **Amazon SNS**:
     - Create an SNS topic for notifications.
     - Subscribe your email address to the SNS topic.
    
## Steps to Run the Project

1. **Set up the hardware**:
   - Connect the YL-69 sensor to the Raspberry Pi using the jumper cables.
   - Power up the Raspberry Pi and ensure it’s connected to the network.

2. **Configure AWS IoT Core**:
   - Create a new thing in the **AWS IoT Core Console** and download the device certificates.
   - Set up an IoT policy that allows publishing to the `moistureSensor` topic.

3. **Deploy Lambda Function**:
   - Create a Lambda function to process the data and send email notifications via SNS.
   - Ensure the Lambda function has the necessary permissions to access SNS.

4. **Configure SNS**:
   - Set up an SNS topic to send email notifications.
   - Subscribe your email address to the SNS topic.

5. **Install and Configure the Python Script**:
   - Install necessary libraries on the Raspberry Pi: `RPi.GPIO` for GPIO and `AWSIoTPythonSDK` for MQTT.
   - Modify the Python script with the correct AWS IoT credentials and MQTT topic.
   - Run the script or set up a cron job to run it periodically.

6. **Run**
   - Run `moisture-notifs.py` from the RaspberryPi, ensure config file exists and holds necessary paths to certificates
   - Subscribe to this topic and check IoT MQTT Test Client is receiving the data
   - Ensure there exists a Rule to trigger the Lambda function
   - Receiving an email alert if the plant is dry is confirmation of the working plant notification system! 

## Contributors
- Project Author: **Colleen Lemak**

