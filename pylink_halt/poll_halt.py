import time
import argparse
import ctypes
import random
import pylink

class TargetHaltError(Exception):
    def __init__(self, message="Target could not be halted"):
        self.message = message
        super().__init__(self.message)

# Create a command line parser
parser = argparse.ArgumentParser(description="Run J-Link Script this periodically try's to hold the CPU and then resume target.")
parser.add_argument("-f", "--firmwarefile", type=str, help="If present the firmware is flashed onto the target.")
parser.add_argument("-d", "--device", type=str, required=True, help="Specify the target device (e.g., STM32H743ZI)")

# Parse command line arguments
args = parser.parse_args()
# Connect JLink Device

while True:
    my_jlink = pylink.JLink()
    my_jlink.open()
    if my_jlink.opened():
        break

# Set the device type and connect
my_jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)

while True:
    try:
        my_jlink.connect(args.device)
    except:
        pass
    if my_jlink.target_connected():
        break

try:
    cycle = 0 
    # J-Link flash script (execute once at the beginning)
    if args.firmwarefile:
        my_jlink.erase()
        # Specify the firmware file path
        my_jlink.flash_file(args.firmwarefile, 0)

    # Infinite loop for the J-Link Read Register script
    while True:
        print("--------------")
        is_halted = my_jlink.halt()
        if not is_halted:
            raise TargetHaltError()

        for i in range(11, 16):
            value = my_jlink.register_read(i)
            unsigned_value = ctypes.c_ulong(value).value
            print(f"R{i:02d}: 0x{unsigned_value:08X}", end=",")
        print(f" cycle_cnt: {cycle}")
        cycle += 1
        my_jlink.restart()
        time.sleep(random.uniform(.1,.2))

except Exception as e:
    print(f"Exception raised: {e}")
    while True:
        pass

# Close the J-Link connection outside the try block
if my_jlink:
    my_jlink.close()
