from rfsocket import Esp8266Timings, RFSocket


class RemoteGroup:
    def __init__(self, rf_pin):
        self._rf_pin = rf_pin
        self._remotes = {}

    def remote(self, remote_id_str):
        remote_id = int(remote_id_str)
        if remote_id not in self._remotes:
            self._remotes[remote_id] = RFSocket(
                self._rf_pin,
                RFSocket.ANSLUT,
                remote_id=remote_id,
                timings=Esp8266Timings
            )
        return self._remotes[remote_id]

    def switch_on(self, remote_id_str, switch_num_str):
        switch_num = int(switch_num_str)
        r = self.remote(remote_id_str)
        r.on(switch_num)
        return r.status()

    def switch_off(self, remote_id_str, switch_num_str):
        switch_num = int(switch_num_str)
        r = self.remote(remote_id_str)
        r.off(switch_num)
        return r.status()

    def group_on(self, remote_id_str):
        r = self.remote(remote_id_str)
        r.group_on()
        return r.status()

    def group_off(self, remote_id_str):
        r = self.remote(remote_id_str)
        r.group_off()
        return r.status()

    def remote_status(self, remote_id_str):
        r = self.remote(remote_id_str)
        return r.status()

    def remotes(self):
        return self._remotes.keys()
