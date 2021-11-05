from twilio.rest import Client as SMSSenderClient


def get_sender_client(account_sid, auth_token):
    return SMSSenderClient(account_sid, auth_token)
