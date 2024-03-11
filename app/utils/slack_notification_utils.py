import os
import requests
import json
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

def send_slack_message(payload):
    """Send a Slack message to a channel via a webhook. 
    
    Args:
        payload (dict): Dictionary containing Slack message, i.e. {"text": "This is a test"}    
    Returns:
        HTTP response code, i.e., <Response [503]>
    """
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')  # Use get to avoid KeyError

    if not webhook_url:
        raise HTTPException(status_code=400, detail="Slack URL not configured.")
    
    headers = {
        'Content-Type': 'application/json',  # Specify the content type
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    return response