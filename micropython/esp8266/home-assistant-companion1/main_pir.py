from umqtt.robust import MQTTClient
from machine import Pin
import time
from webrepl import start
start()

mqtt = MQTTClient(b"sensor_pir", "kosteczka.local")
mqtt.connect()

value_to_send = None


def cb(pin):
    global value_to_send
    value_to_send = pin.value()


p = Pin(4, Pin.IN)
p.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=cb)

while True:
    if value_to_send is None:
        time.sleep(0.1)
        continue
    mqtt.publish(b"home/sensor/pir/1", str(value_to_send))
    value_to_send = None
