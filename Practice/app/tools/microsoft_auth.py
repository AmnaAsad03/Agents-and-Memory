import os

import msal
from dotenv import load_dotenv


load_dotenv()


CLIENT_ID = os.getenv("CLIENT_ID")
AUTHORITY = os.getenv("AUTHORITY")

SCOPES = [
    "Mail.Send"
]


def get_access_token():
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )

    accounts = app.get_accounts()

    if accounts:
        result = app.acquire_token_silent(
            SCOPES,
            account=accounts[0],
        )

        if result and "access_token" in result:
            return result["access_token"]

    result = app.acquire_token_interactive(
        scopes=SCOPES
    )

    if "access_token" in result:
        return result["access_token"]

    raise Exception(
        f"Authentication failed: "
        f"{result.get('error_description')}"
    )