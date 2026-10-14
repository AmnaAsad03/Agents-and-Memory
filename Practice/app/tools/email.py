import requests
from langchain_core.tools import tool
from app.tools.microsoft_auth import get_access_token


@tool
def draft_email(recipient: str, subject: str, body: str) -> dict:
    """Create an email draft."""
    return {
        "recipient": recipient,
        "subject": subject,
        "body": body,
    }


def send_email(email: dict) -> bool:
    token = get_access_token()

    payload = {
        "message": {
            "subject": email["subject"],
            "body": {
                "contentType": "Text",
                "content": email["body"],
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": email["recipient"],
                    }
                }
            ],
        }
    }

    response = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )

    if response.status_code != 202:
        raise Exception(
            f"Email sending failed: {response.status_code} - {response.text}"
        )

    return True