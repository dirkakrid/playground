
from machine import I2C, Pin
from umqtt.robust import MQTTClient
from bme280 import BME280
from time import sleep
from ujson import dumps

i2c = I2C(scl=Pin(5), sda=Pin(4))
mqtt = MQTTClient(b"sensor_bme280", "kosteczka.local")
bme = BME280(i2c=i2c)
mqtt.connect()

while True:
    t, p, h = bme.values
    msg = dumps({
        "temperature": float(t[:-1]),
        "pressure": float(p[:-3]),
        "humidity": float(h[:-1]),
    })
    mqtt.publish(b"home/sensor/bme280/1", msg)
    sleep(120)
