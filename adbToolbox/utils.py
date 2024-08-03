import subprocess
import sys
import os
import time
import logging
import cv2
import numpy as np

keyCode = {
    "KEYCODE_UNKNOWN": 0,
    "KEYCODE_MENU": 1,
    "KEYCODE_SOFT_RIGHT": 2,
    "KEYCODE_HOME": 3,
    "KEYCODE_BACK": 4,
    "KEYCODE_CALL": 5,
    "KEYCODE_ENDCALL": 6,
    "KEYCODE_0": 7,
    "KEYCODE_1": 8,
    "KEYCODE_2": 9,
    "KEYCODE_3": 10,
    "KEYCODE_4": 11,
    "KEYCODE_5": 12,
    "KEYCODE_6": 13,
    "KEYCODE_7": 14,
    "KEYCODE_8": 15,
    "KEYCODE_9": 16,
    "KEYCODE_STAR": 17,
    "KEYCODE_POUND": 18,
    "KEYCODE_DPAD_UP": 19,
    "KEYCODE_DPAD_DOWN": 20,
    "KEYCODE_DPAD_LEFT": 21,
    "KEYCODE_DPAD_RIGHT": 22,
    "KEYCODE_DPAD_CENTER": 23,
    "KEYCODE_VOLUME_UP": 24,
    "KEYCODE_VOLUME_DOWN": 25,
    "KEYCODE_POWER": 26,
    "KEYCODE_CAMERA": 27,
    "KEYCODE_CLEAR": 28,
    "KEYCODE_A": 29,
    "KEYCODE_B": 30,
    "KEYCODE_C": 31,
    "KEYCODE_D": 32,
    "KEYCODE_E": 33,
    "KEYCODE_F": 34,
    "KEYCODE_G": 35,
    "KEYCODE_H": 36,
    "KEYCODE_I": 37,
    "KEYCODE_J": 38,
    "KEYCODE_K": 39,
    "KEYCODE_L": 40,
    "KEYCODE_M": 41,
    "KEYCODE_N": 42,
    "KEYCODE_O": 43,
    "KEYCODE_P": 44,
    "KEYCODE_Q": 45,
    "KEYCODE_R": 46,
    "KEYCODE_S": 47,
    "KEYCODE_T": 48,
    "KEYCODE_U": 49,
    "KEYCODE_V": 50,
    "KEYCODE_W": 51,
    "KEYCODE_X": 52,
    "KEYCODE_Y": 53,
    "KEYCODE_Z": 54,
    "KEYCODE_COMMA": 55,
    "KEYCODE_PERIOD": 56,
    "KEYCODE_ALT_LEFT": 57,
    "KEYCODE_ALT_RIGHT": 58,
    "KEYCODE_SHIFT_LEFT": 59,
    "KEYCODE_SHIFT_RIGHT": 60,
    "KEYCODE_TAB": 61,
    "KEYCODE_SPACE": 62,
    "KEYCODE_SYM": 63,
    "KEYCODE_EXPLORER": 64,
    "KEYCODE_ENVELOPE": 65,
    "KEYCODE_ENTER": 66,
    "KEYCODE_DEL": 67,
    "KEYCODE_GRAVE": 68,
    "KEYCODE_MINUS": 69,
    "KEYCODE_EQUALS": 70,
    "KEYCODE_LEFT_BRACKET": 71,
    "KEYCODE_RIGHT_BRACKET": 72,
    "KEYCODE_BACKSLASH": 73,
    "KEYCODE_SEMICOLON": 74,
    "KEYCODE_APOSTROPHE": 75,
    "KEYCODE_SLASH": 76,
    "KEYCODE_AT": 77,
    "KEYCODE_NUM": 78,
    "KEYCODE_HEADSETHOOK": 79,
    "KEYCODE_FOCUS": 80,
    "KEYCODE_PLUS": 81,
    "KEYCODE_MENU": 82,
    "KEYCODE_NOTIFICATION": 83,
    "KEYCODE_SEARCH": 84,
    "TAG_LAST_KEYCODE": 85
}

if os.name == 'nt':
    adb = ".\\tools\\adb.exe"
else:
    adb = "./tools/adb.exe"
    
class Control:
    def __init__(self, id: str, model: str = "", shell: object = None):
        self.id = id
        self.model = model
        self.shell = shell
        return None
    
    def tap(self, x: int, y: int) -> None:
        if (x == 0) and (y == 0):
            return None

        cmd = '"input" "tap" "{x}" "{y}"'.format(type = type, x = x, y = y)
        logging.warning("{device}: tap (x = {x}, y = {y})".format(device = self.id, x = x, y = y))
        self.shell(cmd)
        return None
    
    def swipe(self) -> None:
        
        return None

    def keyEvent(self, event_code: int) -> None:
        if event_code:
            try:
                int(event_code)
            except ValueError:
                raise ValueError("wrong keyevent, found [{}]".format(event_code))
            cmd = '"input" "keyevent" "{event}"'.format(type = type, event = event_code)
            logging.warning("{device}: keyevent ({event})".format(device = self.id, event = event_code))
            self.shell(cmd)
        return None

    def inputText(self, text: str) -> None:
        if text:
            logging.warning("{device}: text ({text})".format(device = self.id, text = text))
            text = text.split(' ')
            for i in range(0, len(text), 1):
                t = text[i]
                cmd = '"input" "text" {text}'.format(type = type, text = t)
                self.shell(cmd)
                
                if not (i == len(text) - 1):
                    self.keyEvent(62)
        return None

class Device:
    def __init__(self, id: str, model: str = "") -> None:
        self.id = id
        self.model = model
        self.Control = Control(id, model, self.shell)
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
        __time = time.time()
        cmd = '{adb} "-s" "{device}" "exec-out" "screencap" "-p"'.format(adb = adb, device = self.id)
        result = subprocess.check_output(cmd, shell=True)
        if result:
            logging.warning("{device}: success capture device (size = {size} kb) in {sec}".format(device = self.id, size = round(len(result) / 1024, 3), sec = str(round(time.time() - __time, 3)) + " sec"))
        return result
        
    def findXY(self, path_img: str) -> list:
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
                x = x + 15
                y = y + 15
                logging.warning("{device}: found '{file}' (x = {x}, y = {y})".format(file = path_img, x = x, y = y, device = self.id))
                return [x, y]
            else:
                logging.warning("{device}: not found '{file}'".format(file = path_img, device = self.id))
                return [0, 0]
        except Exception as ex:
            raise ex
        return [0, 0]

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
                    devices.append(Device(i[0], subprocess.getoutput(cmd)))
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
