import subprocess
import sys
import os
import time
import logging
import cv2
import numpy as np

debug = True

if os.name == 'nt':
    adb = ".\\tools\\adb.exe"
else:
    adb = "./tools/adb.exe"

class device:
    def __init__(self, id: str, model: str = "") -> None:
        self.id = id
        self.model = model
        return None

    def __repr__(self) -> str:
        if self.model:
            return "{} ({})".format(self.id, self.model)
        return self.id

    def __call__(self) -> None:
        os.system('{adb} "-s" "{device}" "shell"'.format(adb = adb, device = self.id))
        return None

    def shell(self, s: str) -> str:
        if not self.id:
            raise TypeError("device is undefined")
        cmd = '{adb} "-s" "{device}" "shell" {cmd}'.format(adb = adb, device = self.id, cmd = s)
        result = subprocess.getoutput(cmd)
        if "device '{device}' not found".format(device = self.id) in result:
            raise TypeError(result)

        return result

    def capture(self) -> bytes:
        global debug
        __time = time.time()
        cmd = '{adb} "-s" "{device}" "exec-out" "screencap" "-p"'.format(adb = adb, device = self.id)
        result = subprocess.check_output(cmd, shell=True)
        if result:
            logging.warning("{device}: success capture device (size = {size} kb) in {sec}".format(device = self.id, size = round(len(result) / 1024, 3), sec = str(round(time.time() - __time, 3)) + " sec"))
        return result

    def input(self, type: str, x: int, y: int) -> None:
        global debug
        if (x == 0) and (y == 0):
            return None

        cmd = '"input" "{type}" "{x}" "{y}"'.format(type = type, x = x, y = y)
        logging.warning("{device}: {type} (x = {x}, y = {y})".format(device = self.id, type = type, x = x, y = y))
        self.shell(cmd)
        return None

    def findXY(self, path_img: str):
        try:
            img = self.capture()

            main_image_array = np.frombuffer(img, np.uint8)

            main_image = cv2.imdecode(main_image_array, cv2.IMREAD_COLOR)
            template_image = cv2.imread(path_img)

            main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

            w, h = template_gray.shape[::-1]

            res = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)

            threshold = 0.75

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val >= threshold:
                x, y = max_loc
                logging.warning("{device}: found '{file}' (x = {x}, y = {y})".format(file = path_img, x = x, y = y, device = self.id))
                return x, y
            else:
                logging.warning("{device}: not found '{file}'".format(file = path_img, device = self.id))
                return 0, 0
        except Exception as ex:
            raise ex
        return 0, 0

def getDevices() -> list:
    logging.warning("adb get devices....")
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
                    cmd = '{adb} "-s" "{id}" "shell" "getprop" "ro.product.model"'.format(adb = adb, id = i[0])
                    devices.append(device(i[0], subprocess.getoutput(cmd)))
    else:
        raise MemoryError("adb not working")
    logging.warning("found {} device".format(len(devices)))
    return devices

def killServer() -> None:
    logging.warning("adb kill server...")
    cmd = '{adb} kill-server'.format(adb = adb)
    subprocess.getoutput(cmd)
    cmd = "taskkill /f /im adb.exe"
    subprocess.getoutput(cmd)
    return None

def adbPair(ipAddress: str, pairCode: int) -> None:
    logging.warning("pairing to {ip}".format(ip = ipAddress))
    cmd = '{adb} "pair" "{ip}"'.format(adb = adb, ip = ipAddress)
    
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)    
    stdout_ = p.communicate(input=str(pairCode).encode('utf8'))[0]
    if 'Successfully paired to {ip}'.format(ip = ipAddress).encode('utf8') in stdout_:
        logging.warning("paired to {ip}".format(ip = ipAddress))
    else:
        logging.warning("cannot pair to {ip}".format(ip = ipAddress))
    return None

def adbConnect(ipAddress: str) -> None:
    logging.warning("connecting to {ip}".format(ip = ipAddress))
    cmd = '{adb} "connect" "{ip}"'.format(adb = adb, ip = ipAddress)
    p = subprocess.getoutput(cmd)
    if "connected to {ip}".format(ip = ipAddress) in p:
        logging.warning("connected to {ip}".format(ip = ipAddress))
    else:
        logging.warning("cannot connect to {ip}".format(ip = ipAddress))
    return None

def adbDisconnect() -> None:
    cmd = '{adb} disconnect'.format(adb = adb)
    subprocess.getoutput(cmd)
    return None
