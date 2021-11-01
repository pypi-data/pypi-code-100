"""
HiveMind NFC reader client
"""
import json
import logging
import signal
import sys
import threading
import time
from datetime import datetime, timedelta

import nfc
import requests
import RPi.GPIO as GPIO
import websocket

__version__ = "0.0.2"

API_BASE_URL = "https://kqhivemind.com/api"
API_URL = f"{API_BASE_URL}/user/signin/nfc/"
WS_URL = "wss://kqhivemind.com/ws/signin"

state = {
    "card": None,
    "time": None,
    "register_user_id": None,
    "register_time": None,
    "cabinet_id": None,
    "listening_pins": set(),
}

with open(sys.argv[1]) as in_file:
    settings = json.load(in_file)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s]  %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

if settings.get("log_file"):
    file_handler = logging.FileHandler(settings.get("log_file"))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    for pin in settings["pin_config"]:
        if pin.get("button"):
            GPIO.setup(pin["button"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if pin.get("light"):
            GPIO.setup(pin["light"], GPIO.OUT)

def register_card(card_id, user_id):
    data = {
        "scene_name": settings["scene"],
        "cabinet_name": settings["cabinet"],
        "token": settings["token"],
        "action": "nfc_register_tapped",
        "card": card_id,
        "user": user_id,
    }

    req = requests.post(API_URL, json=data)

def sign_in(card_id, player_id):
    data = {
        "scene_name": settings["scene"],
        "cabinet_name": settings["cabinet"],
        "token": settings["token"],
        "action": "sign_in",
        "card": card_id,
        "player": player_id,
    }

    req = requests.post(API_URL, json=data)

def sign_out(player_id):
    data = {
        "scene_name": settings["scene"],
        "cabinet_name": settings["cabinet"],
        "token": settings["token"],
        "action": "sign_out",
        "player": player_id,
    }

    req = requests.post(API_URL, json=data)

def listen_card():
    def connected(llc):
        logger.info(llc.identifier.hex())
        state["card"] = llc.identifier.hex()
        state["time"] = datetime.now()

        if state["register_user_id"] and state["register_time"] > datetime.now() - timedelta(minutes=1):
            register_card(llc.identifier.hex(), state["register_user_id"])
            state["register_user_id"] = None

        return True

    with nfc.ContactlessFrontend(settings["usb_device"]) as clf:
        while True:
            clf.connect(rdwr={"on-connect": connected})

def on_button_down(channel):
    if GPIO.input(channel) == 0:
        return

    logger.info("Button press on {}".format(channel))
    players = { i["button"]: i["player_id"] for i in settings["pin_config"] }
    player = players.get(channel)
    if player:
        logger.info("Button {} is player {}".format(channel, player))
        if state["card"] and state["time"] > datetime.now() - timedelta(seconds=15):
            sign_in(state["card"], player)
            state["card"] = None
            state["time"] = None
            state["register_user_id"] = None
            state["register_time"] = None
        else:
            sign_out(player)

def listen_buttons():
    for pin in settings["pin_config"]:
        if pin.get("button"):
            while pin.get("button") not in state["listening_pins"]:
                try:
                    logger.info("Listening on pin {} for player {}".format(pin["button"], pin["player_id"]))
                    GPIO.add_event_detect(pin["button"], GPIO.RISING, callback=on_button_down)
                    state["listening_pins"].add(pin["button"])
                except:
                    logger.exception("Could not listen on pin {}".format(pin["button"]))
                    time.sleep(1)

def on_message(ws, message_text):
    try:
        logger.debug(message_text)
        message = json.loads(message_text)
        if message.get("scene_name") != settings["scene"] or message.get("cabinet_name") != settings["cabinet"]:
            return

        if message.get("type") == "nfc_register":
            if message["reader_id"] == settings["reader"]:
                logger.info("Got register request for user ID {}".format(message["user_id"]))
                state["register_user_id"] = message["user_id"]
                state["register_time"] = datetime.now()

        else:
            light_pins = { i["player_id"]: i["light"] for i in settings["pin_config"] }
            pin = light_pins.get(int(message["player_id"]))
            if pin:
                value = GPIO.HIGH if message["action"] == "sign_in" else GPIO.LOW
                logger.info("Setting {} to {} (player {})".format(pin, value, message["player_id"]))
                GPIO.output(pin, value)

    except Exception as e:
        logger.exception("Exception in on_message")

def on_ws_error(ws, error):
    logger.error("Error in websocket connection: {}".format(error))
    ws.close()

def on_ws_close(ws, close_status_code, close_msg):
    logger.error("Websocket closed ({})".format(close_msg))

def set_lights_from_api():
    req = requests.get(f"{API_BASE_URL}/game/scene/", params={"name": settings["scene"]})
    scene_id = req.json()["results"][0]["id"]

    req = requests.get(f"{API_BASE_URL}/game/cabinet/",
                       params={"scene": scene_id, "name": settings["cabinet"]})
    cabinet_id = req.json()["results"][0]["id"]

    req = requests.get(f"{API_BASE_URL}/game/cabinet/{cabinet_id}/signin/")
    signed_in = {i["player_id"] for i in req.json()["signed_in"]}

    for row in settings["pin_config"]:
        value = GPIO.HIGH if row["player_id"] in signed_in else GPIO.LOW
        GPIO.output(row["light"], value)

def listen_ws():
    logger.info("Starting websocket thread.")

    while True:
        try:
            set_lights_from_api()

            wsapp = websocket.WebSocketApp(WS_URL, on_message=on_message, on_error=on_ws_error,
                                           on_close=on_ws_close)
            logger.info("Websocket connection online.")
            wsapp.run_forever()

        except Exception as e:
            logger.exception("Exception in wsapp.run_forever")

        time.sleep(1)


def main():
    setup_gpio()

    card_thread = threading.Thread(target=listen_card, name="card", daemon=True)
    card_thread.start()

    ws_thread = threading.Thread(target=listen_ws, name="websocket", daemon=True)
    ws_thread.start()

    button_thread = threading.Thread(target=listen_buttons, name="buttons", daemon=True)
    button_thread.start()

    while True:
        time.sleep(1)

    logger.info("Exiting.")


if __name__ == "__main__":
    main()

