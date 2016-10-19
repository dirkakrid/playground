
rfsocket.py:
	wget https://raw.githubusercontent.com/wuub/micropython-rfsocket/master/rfsocket.py

libs: rfsocket.py rfsocket boot

%:
	~/git/github/webrepl/webrepl_cli.py  $@.py 192.168.1.61:/$@.py


.PHONY: libs 