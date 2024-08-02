import adbToolbox

devices = adbToolbox.getDevices()

for device in devices:
    x, y = device.findXY('target.png')
    device.input("tap", x, y)
