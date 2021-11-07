from time import sleep, time

from paho.mqtt import client as mqtt
from configparser import ConfigParser

from pedestals.fake_pedestal import FakePedestal
from commands import command_classes
from commands.button import Button

from remotes.azeq6_remote import AZEQ6PedestalRemote
from remotes.fake_pedestal_remote import FakePedestalRemote
#from commands.message_parser import MessageParser
import argparse

""" MQTT call backs:"""
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK.")
    else:
        print("Connection failed with response code " + str(rc))
    client.subscribe("Pi-1")


def on_log(client, userdata, level, buf):
    print("log:" + buf)


def on_subscribe(client, userdata, mid, granted_qos):
    print("<<Subscription  successful.>>")


def on_message(client, userdata, msg_enc):
    time_rec = time()
    msg = msg_enc.payload.decode("UTF-8")
    print("Message received: " + msg)
    select_button(msg, time_rec)

#def mqtt_monitor_thread():


""" Creating commands:"""
def commands_init(pedestal_device):
    debug_command = command_classes.ToggleDebug(pedestal_device)
    global debug_pressed
    debug_pressed = Button(debug_command)

    stop_command = command_classes.StopSlew(pedestal_device)
    global stop_pressed
    stop_pressed = Button(stop_command)

    sweep_on_command = command_classes.SweepOn(pedestal_device)
    global sweep_pressed
    sweep_pressed = Button(sweep_on_command)

    calibrate_command = command_classes.Calibrate(pedestal_device)
    global calibrate_pressed
    calibrate_pressed = Button(calibrate_command)


    slew_command = command_classes.StartSlew(pedestal_device)
    global slew_pressed
    slew_pressed = Button(slew_command)

    get_coords_command = command_classes.GetOrientation(pedestal_device)
    global get_coords_pressed
    get_coords_pressed = Button(get_coords_command)


    goto_az_el_command = command_classes.GoToAzEl(pedestal_device)
    global goto_az_el_pressed
    goto_az_el_pressed = Button(goto_az_el_command)

    goto_location_command = command_classes.GoToLocation(pedestal_device)
    global goto_location_pressed
    goto_location_pressed = Button(goto_location_command)

def select_button(msg, time_rec):
    mqtt_cmds = {"calibrate": "CALIB", "stop": "STOP", "slew": "SLEW", "goto_location": "GOTO-LOC",
                 "goto_az_el": "GOTO-AZEL",  "sweep": "SWEEP", "get_pos": "GET-AZ-EL", "timing": "TIMING-TEST"
                 }
    msg_list = msg.split("/")
    if msg_list[0] == mqtt_cmds["calibrate"]:
        calibrate_pressed.press()
    elif msg_list[0] == mqtt_cmds["stop"]:
        stop_pressed.press()
    elif msg_list[0] == mqtt_cmds["slew"]:
        axis = 0
        dir = 0
        if msg_list[1] == "AZ":
            axis = 1
        else:
            axis = 2
        if msg_list[2] == "POS":
            dir = 1
        else: # msg_list[2] = "NEG"
            dir = 2
        slew_pressed.press(axis, dir)
    elif msg_list[0] == mqtt_cmds["goto_az_el"]:
        az = float(msg_list[1])
        el = float(msg_list[2])
        goto_az_el_pressed.press(az, el)
    elif msg_list[0] == mqtt_cmds["goto_location"]:
        lat = float(msg_list[1])
        long = float(msg_list[2])
        alt = float(msg_list[3])
        goto_location_pressed.press(lat, long, alt)
    elif msg_list[0] == mqtt_cmds["sweep"]:
        sweep_pressed.press()
    elif msg_list[0] == mqtt_cmds["timing"] and debug:
        time_sent = float(msg_list[1])
        time_elapsed = (time_rec - time_sent)*1000
        print("Time taken to receive test message: {} ms".format(time_elapsed))
        with open("mqtt_latency.txt", "a+") as f:
            f.write(str(time_elapsed) + "\n")



def main():

    # Instantiate pedestal controller object:
    try:
        pc = AZEQ6PedestalRemote.get_pedestal_device()
    except Exception as e:
        pc = FakePedestalRemote.get_pedestal_device()

    commands_init(pc)


    if args.debug_flag:
        global debug
        debug = True
        debug_pressed.press()  # check if debug mode entered
        print("--Debug Mode Active--")


    cf = ConfigParser()
    cf.read("config.ini")

    broker = cf["MQTT"]["Broker"]
    pi_client = cf["MQTT"]["client_name"]
    client = mqtt.Client("Pi-1", protocol=mqtt.MQTTv31)

    # bind callbacks:
    client.on_connect = on_connect
    client.on_log = on_log
    client.on_subscribe = on_subscribe
    client.on_message = on_message


    #pc = PedestalController(FakeControllerClient(), FakeGPSClient())
    try:
        #client.connect(host="localhost", port=1883)
        client.connect(host="localhost", port=1883) # "169.254.228.235"
    except Exception as e:
        print(e)

    client.loop_start() # start mqtt client loop
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Quitting...")
        SystemExit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug',
        action='store_true',
        dest="debug_flag",
        help='toggle debug mode'
    )
    args = parser.parse_args()

    main()





