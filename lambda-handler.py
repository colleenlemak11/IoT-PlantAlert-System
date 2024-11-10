# Author: Colleen Lemak
# File: lambda-handler.py
# Objective: Leverage Internet of Things and AWS to create plant-watering reminder alert system via email notifications.
#            Implements logic for PlantAlert in conjunction with an AWS Lambda function.

import json
import boto3
from config import ARN

# Initialize SNS client
sns_client = boto3.client('sns')
sns_topic_arn = ARN

def lambda_handler(event, context):
    # Extract moisture status from the event
    # Format: {"moisture": {"dry"}}
    moisture_data = event['moisture']

    # Check if the soil is dry
    if moisture_data == "dry":
        # Define the message
        message = {
            "default": "Your plant's soil is dry. Please water the plant! :)"
        }
        # Configure the publish to SNS
        sns_client.publish(
            TargetArn=sns_topic_arn,
            Message=json.dumps(message),
            MessageStructure='json',
            Subject="PlantAlert: Soil Moisture Level is Low"
        )
        return {"status": "Alert sent for dry soil."}

    return {"status": "No alert needed, soil moisture adequate."}