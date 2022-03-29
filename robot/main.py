# import motors
import base64
import math
from io import BytesIO

from tether import Tether
import asyncio
# import linear_actuator
import sys
from vision import Detector, Locator
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
        print('STOPPING')
        quit()
        # t.send(f'R:{input("Enter X")}, {input("Enter Y")}, {input("Enter Angle (Degrees)")}
    if cmd == 'G':
        print("revied gamepadChanges: " + args[0])
        controllerReceiver.update(args[0])
        print(str(controllerReceiver))


# begin accepting connections
loop = asyncio.get_event_loop()
t = Tether(handler=receive_msg, loop=loop)


# detector = Detector()
# locator = Locator()

async def sendCords():
    while True:
        # print('pp')
        await t.send(f'R:{x},{y},{angle}')
        await asyncio.sleep(1.0)


async def sendImages():
    while True:
        im = Image.open('rick-astley-rickrolling.jpg')
        im = im.resize((176, 144), )  # 144p

        im_file = BytesIO()
        im.save(im_file, format="JPEG")
        im_bytes = im_file.getvalue()  # i
        im_b64 = base64.b64encode(im_bytes)

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
        if i % 10 == 0:
            print("\n--- READ XBOX VALUES ---")
            pos_cmd = f'R:{controllerReceiver.leftStickX()},{controllerReceiver.leftStickY()},{math.atan2(controllerReceiver.rightStickY(), controllerReceiver.rightStickX()) - math.radians(90)}'
            await t.send(pos_cmd)
            print(f"LX: {controllerReceiver.leftStickX()}")
            print(f"LY: {controllerReceiver.leftStickY()}")
            print(
                f"R Angle: {math.degrees(math.atan2(controllerReceiver.rightStickY(), controllerReceiver.rightStickX()))}")
            print("------------------------\n")
            i = 0
        await asyncio.sleep(0.01)
        i += 1


# loop.create_task(sendCords())
loop.create_task(sendImages())
# loop.create_task(lidar_test())
# loop.create_task(manual_control())

# Start the event loop
cprint(f"IP Address: {t.get_ip_address()}", "cyan")
print("Starting event loop")
loop.run_forever()

# Create obstacle detector
# detector = Detector()

# while True:
#     sleep(1)
#     print(cmd + "\n\n")
