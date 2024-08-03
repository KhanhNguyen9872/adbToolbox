import adbToolbox

adbToolbox.killServer()
# adbToolbox.adbPair("192.168.1.8:40775", "343981")
# adbToolbox.adbConnect("192.168.1.8:39823")

devices = adbToolbox.getDevices()

print("All devices:", devices)

for device in devices:
    x, y = device.findXY('target.png')
    device.input("tap", x, y)
