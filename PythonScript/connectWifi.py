import network

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("raspi-webgui","ChangeMe")
if (station.isconnected()):
	print("ESP connected")

