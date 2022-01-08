from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
from blinkpy.helpers.util import json_load

BlinkAccount = Blink()
auth = Auth(json_load("creds.json"))
BlinkAccount.auth = auth
BlinkAccount.start()

SYNC_MODULE_NAME = "Home1"
CAMERA1 = "Camera1"
CAMERA2 = "New Camera"

def disarm_module():
    BlinkAccount.sync[SYNC_MODULE_NAME].arm = False

def arm_module():
    BlinkAccount.sync[SYNC_MODULE_NAME].arm = True
