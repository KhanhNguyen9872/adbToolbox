import subprocess
import sys
import os
import logging
import cv2
import numpy as np

# logging.disable(logging.WARNING)

if os.name == 'nt':
    adb = ".\\tools\\adb.exe"
else:
    adb = "./tools/adb.exe"

class device:
    def __init__(self, id: str) -> None:
        self.id = id
        return None

    def __repr__(self) -> str:
        return self.id

    def __call__(self) -> None:
        os.system('{adb} "-s" "{device}" "shell"'.format(adb = adb, device = self.id))
        return None

    def shell(self, s: str) -> str:
        if not self.id:
            logging.error("device is undefined")
        cmd = '{adb} "-s" "{device}" "shell" {cmd}'.format(adb = adb, device = self.id, cmd = s)
        result = subprocess.getoutput(cmd)
        if "device '{device}' not found".format(device = self.id) in result:
            logging.error(result)
            return ""
        return result

    def capture(self) -> bytes:
        cmd = '{adb} "-s" "{device}" "exec-out" "screencap" "-p"'.format(adb = adb, device = self.id)
        result = subprocess.check_output(cmd, shell=True)
        if result:
            logging.warning("{device}: success capture device (size = {size})".format(device = self.id, size = len(result)))
        return result

    def input(self, type: str, x: int, y: int) -> None:
        if (x == 0) and (y == 0):
            return None

        cmd = '"input" "{type}" "{x}" "{y}"'.format(type = type, x = x, y = y)
        logging.warning("{device}: {type} {x}, {y}".format(device = self.id, type = type, x = x, y = y))
        self.shell(cmd)
        return None

    def findXY(self, path_img):
        img = self.capture()

        main_image_array = np.frombuffer(img, np.uint8)

        main_image = cv2.imdecode(main_image_array, cv2.IMREAD_COLOR)
        template_image = cv2.imread(path_img)

        main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

        w, h = template_gray.shape[::-1]

        res = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        threshold = 0.7

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= threshold:
            x, y = max_loc
            logging.warning("{device}: found '{file}' [{x}, {y}]".format(file = path_img, x = x, y = y, device = self.id))
            return x, y
        else:
            logging.warning("{device}: not found '{file}'".format(file = path_img, device = self.id))
            return 0, 0

def getDevices() -> list:
    cmd = "{adb} devices".format(adb = adb)
    result = subprocess.getoutput(cmd)
    devices = []
    if result:
        result = result.split("\n")[1:]
        for i in result:
            if i:
                if "*" == i[0] or "List of devices attached" in i:
                    continue
                i = i.split('\t')
                if i[1] == 'device' or i[1] == 'offline':
                    devices.append(device(i[0]))
    else:
        raise MemoryError("adb not working")
    return devices

def kill_server() -> None:
    cmd = '{adb} kill-server'.format(adb = adb)
    subprocess.getoutput(cmd)
    return None
