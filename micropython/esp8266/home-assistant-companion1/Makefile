
rfsocket.py:
	wget https://raw.githubusercontent.com/wuub/micropython-rfsocket/master/rfsocket.py

libs: rfsocket.py rfsocket boot bme280 ssd1306 binascii

%.mpy:
	~/git/github/micropython/mpy-cross/mpy-cross $(basename $@).py

cred:
	~/git/github/webrepl/webrepl_cli.py  wifi.credentials ${WEBREPL_ADDR}:/wifi.credentials

main_%:
	~/git/github/webrepl/webrepl_cli.py  $@.py ${WEBREPL_ADDR}:/main.py


%: %.mpy
	~/git/github/webrepl/webrepl_cli.py  $@.mpy ${WEBREPL_ADDR}:/$@.mpy

clean:
	rm -f *.mpy


all: cred libs

.PHONY: libs cred all clean