from getpass import getpass
from typing import Optional

from aibro.constant import IS_DEMO
from aibro.tools.prints import print_err
from aibro.tools.service.api_service import aibro_client
from aibro.tools.utils import sha256_encode

AUTHENTICATED_USER_ID = None


def check_authentication() -> Optional[str]:
    global AUTHENTICATED_USER_ID
    if not AUTHENTICATED_USER_ID:
        if IS_DEMO:
            email = input("Welcome! To launch a trial, please enter your email: ")
            data = {"email": email, "password": "demo"}
        else:
            email = input("Enter your email: ")
            password = getpass()
            encoded = sha256_encode(password)
            data = {"email": email, "password": encoded}
        try:
            resp = aibro_client.post_with_json_data("v1/authenticate", data)
            AUTHENTICATED_USER_ID = resp.json()["user_id"]
            print("Thanks! Please open https://aipaca.ai/jobs to track job status.")
        except Exception as e:
            print_err(f"Authentication Error: {str(e)}")
            return None
    else:
        if IS_DEMO:
            print("Already entered email!")
        else:
            print("Already authenticated!")

    return AUTHENTICATED_USER_ID
