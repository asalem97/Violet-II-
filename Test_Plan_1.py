#Violet II Test Plan 1
#Created by Scott McCann 
#February 10, 2025


import gpiod
import time

GPIO_CHIP = "gpiochip3"
GPIO_LINE = 10  # P1_2

# Release GPIO if already in use
chip = gpiod.Chip(GPIO_CHIP)
line = chip.get_line(GPIO_LINE)
try:
    # If the GPIO is already requested, release it first
    if line.consumer():
        print("GPIO is already in use. Releasing it first...")
        line.release()
        time.sleep(1)  # Wait a moment before re-requesting

    # Request GPIO for control
    line.request(consumer="P1_2_Control", type=gpiod.LINE_REQ_DIR_OUT)

    while True:
        print("P1_2 HIGH")
        line.set_value(1)
        time.sleep(2)

        print("P1_2 LOW")
        line.set_value(0)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    print("Releasing GPIO")
    line.release()
