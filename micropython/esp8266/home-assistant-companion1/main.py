from machine import Pin
from rfsocket import Esp8266Timings, RFSocket

REMOTES = {}
rf_pin = Pin(0, Pin.OUT)


def remote(remote_id_str):
    remote_id = int(remote_id_str)
    if remote_id not in REMOTES:
        REMOTES[remote_id] = RFSocket(rf_pin, RFSocket.ANSLUT, remote_id=remote_id, timings=Esp8266Timings)
    return REMOTES[remote_id]


def switch_on(remote_id_str, switch_num_str):
    switch_num = int(switch_num_str)
    r = remote(remote_id_str)
    r.on(switch_num)
    return r.status()


def switch_off(remote_id_str, switch_num_str):
    switch_num = int(switch_num_str)
    r = remote(remote_id_str)
    r.off(switch_num)
    return r.status()


def group_on(remote_id_str):
    r = remote(remote_id_str)
    r.group_on()
    return r.status()


def group_off(remote_id_str):
    r = remote(remote_id_str)
    r.group_off()
    return r.status()


def remote_status(remote_id_str):
    r = remote(remote_id_str)
    return r.status()


def remotes():
    return REMOTES.keys()
