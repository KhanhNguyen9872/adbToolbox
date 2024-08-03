import adbToolbox
import time

adbToolbox.killServer()

# adbToolbox.adbPair("192.168.1.8:40775", "343981")
# adbToolbox.adbConnect("192.168.1.8:39823")

devices = adbToolbox.getDevices()

print("All devices:", devices)

for device in devices:
    x, y = device.findXY('1.png')
    device.Control.tap(x, y)
    
    time.sleep(1)
    
    x, y = device.findXY('2.png')
    device.Control.tap(x, y)
    
    time.sleep(1)
    
    device.Control.inputText("hello world!")
    
    device.Control.keyEvent(adbToolbox.keyCode["KEYCODE_ENTER"])
