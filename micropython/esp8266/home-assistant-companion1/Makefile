main:
	~/git/github/webrepl/webrepl_cli.py  main.py 192.168.1.61:/main.py


rfsocket.py:
	wget https://raw.githubusercontent.com/wuub/micropython-rfsocket/master/rfsocket.py

libs: rfsocket.py
	~/git/github/webrepl/webrepl_cli.py  boot.py 192.168.1.61:/boot.py
	~/git/github/webrepl/webrepl_cli.py  rfsocket.py 192.168.1.61:/rfsocket.py


.PHONY: libs main