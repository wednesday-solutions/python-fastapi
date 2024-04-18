from __future__ import annotations

import json

import requests
from fastapi import HTTPException

from app.config.base import settings


def send_slack_message(payload):
    """Send a Slack message to a channel via a webhook.

    Args:
        payload (dict): Dictionary containing Slack message, i.e. {"text": "This is a test"}
    Returns:
        HTTP response code, i.e., <Response [503]>
    """
    if not settings.SLACK_WEBHOOK_URL:
        return

    webhook_url = settings.SLACK_WEBHOOK_URL

    if not webhook_url:
        raise HTTPException(status_code=400, detail="Slack URL not configured.")

    headers = {
        "Content-Type": "application/json",  # Specify the content type
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    return response
