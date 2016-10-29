from umqtt.robust import MQTTClient
from machine import Pin, unique_id
from remote_group import RemoteGroup
import ubinascii as binascii

rf_pin = Pin(0, Pin.OUT)
rg = RemoteGroup(rf_pin)

client_id = b"wemos_" + binascii.hexlify(unique_id())
mqtt_host = "kosteczka.local"
mqtt = MQTTClient(client_id, mqtt_host)


def handle_message(topic, msg):
    print(topic, msg)
    parts = msg.decode("utf-8").split(" ")
    try:
        getattr(rg, parts[0])(*parts[1:])
    except AttributeError:
        pass
    mqtt.publish(topic[:-3] + "/".join(parts[1:]).encode("utf-8"), msg, retain=True)

mqtt.set_callback(handle_message)
mqtt.connect()
mqtt.subscribe(b"home/rfsocket/set")

print("Waiting on MQTT")
while True:
    mqtt.wait_msg()
