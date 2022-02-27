# import motors
import base64
import math
from io import BytesIO

from tether import Tether
from time import sleep
import asyncio
import random
# import linear_actuator
import sys
from vision import Detector, Locator
from xbox_drive import XboxController
from termcolor import colored, cprint
from ControllerReceiver import ControllerReceiver

from PIL import Image


x = 0
y = 0
angle = 0

controllerReceiver = ControllerReceiver()

def receive_msg(msg, conn):
    # format is operator:arguments
    cmd, *args = msg.split(':')

    print(f"cmd: {cmd}, args: {args}")
    if cmd == 'M':
        global x
        x = input("Enter X")
        global y
        y = input("Enter Y")
        global angle
        angle = math.radians(int(input("Enter Angle (Degrees)")))
    if cmd == 'STOP':
        print('STOPING')
        quit()
        #t.send(f'R:{input("Enter X")}, {input("Enter Y")}, {input("Enter Angle (Degrees)")}
    if cmd[0] == 'G':
        controllerReceiver.update(cmd[1])




# begin accepting connections
loop = asyncio.get_event_loop()
t = Tether(handler=receive_msg, loop=loop)

# detector = Detector()
# locator = Locator()
#xbox = XboxController()


async def sendCords():
    while True:
        #print('pp')
        await t.send(f'R:{x},{y},{angle}')
        await asyncio.sleep(1.0)

async def sendImages():
    while True:
        im = Image.open('rick-astley-rickrolling.jpg')
        im = im.resize((128, 128), )

        im_file = BytesIO()
        im.save(im_file, format="JPEG")
        im_bytes = im_file.getvalue()  # i
        im_b64 = base64.b64encode(im_bytes)

        print(im_b64)
        # await t.send("I:" + str(im_b64)[2:-2])
        await t.send(im_b64)
        await asyncio.sleep(1.0)
async def lidar_test():
    i = 0
    while True:
        locator.locate()
        new_obs = detector.detect(rob_x=locator.x, rob_y=locator.y, rob_a=locator.angle)
        if i % 10 == 0:
            print(f"Detected {len(new_obs)} obstacles")
            print(f"Location: ({locator.x}mm, {locator.y}mm, {locator.angle}rad)")
            i = 0

        obs_strs = [f"{o.x},{o.y}" for o in new_obs]
        obs_cmd = "O:" + ",".join(obs_strs)
        await t.send(obs_cmd)
        await t.send(f"R:{locator.x},{locator.y},{locator.angle}")
        await asyncio.sleep(0.25)
        i += 1


async def manual_control():
    i = 0
    while True:
        xbox.read_controller()
        if i % 10 == 0:
            print("\n--- READ XBOX VALUES ---")
            pos_cmd = f'R:{xbox.motor_xy.x},{xbox.motor_xy.y},{math.degrees(math.atan2(xbox.td_xy.y,xbox.td_xy.x))}'
            await t.send(pos_cmd)
            print(xbox.motor_xy)
            print(xbox.td_xy)
            print("------------------------\n")
            i = 0
        await asyncio.sleep(0.5)
        i += 1


loop.create_task(sendCords())
loop.create_task(sendImages())
#loop.create_task(lidar_test())
#loop.create_task(manual_control())

# Start the event loop
cprint(f"IP Address: {t.get_ip_address()}", "cyan")
print("Starting event loop")
loop.run_forever()

# Create obstacle detector
# detector = Detector()

# while True:
#     sleep(1)
#     print(cmd + "\n\n")
