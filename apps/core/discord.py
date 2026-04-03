"""
Centralised Discord webhook helper.
Called by commissions, contact, and orders whenever a new entry is created.
"""
import logging
import requests

logger = logging.getLogger(__name__)


def send_discord_notification(
    webhook_url: str,
    title: str,
    color: int = 0xFF6B1A,
    fields: list = None,
    description: str = "",
):
    """
    Send a rich-embed message to a Discord webhook.

    Parameters
    ----------
    webhook_url : str
        Full Discord webhook URL from Django settings.
    title : str
        Title shown at the top of the embed card.
    color : int
        Embed sidebar colour as an integer  e.g. 0xFF6B1A (orange).
    fields : list of dict
        Each dict must have keys: name, value, inline (bool).
    description : str
        Optional body text shown below the title.
    """
    if not webhook_url:
        logger.warning("Discord webhook URL is not configured. Skipping.")
        return

    payload = {
        "embeds": [
            {
                "title":       title,
                "description": description,
                "color":       color,
                "fields":      fields or [],
                "footer":      {"text": "Creviz Studio"},
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        logger.info("Discord notification sent: %s", title)
    except requests.exceptions.RequestException as exc:
        logger.error("Discord webhook error: %s", exc)