#Violet II Test Plan 2
#Created by Scott McCann
#February 10, 2025

import time
import os
import subprocess

# Define GPIO pin for Pin 33 on Header 1 (GPIO1_28)
GPIO_PIN = 28

# Export the GPIO pin 
def export_gpio(pin):
	if not os.path.exists(f'/sys/class/gpio/gpio{pin}'):
		with open('/sys/class/gpio/export', 'w') as f:
			f.write(str(pin))

# Set the direction of the GPIO pin 
def set_gpio_direction(pin, direction):
	with open(f'/sys/class/gpio/gpio{pin}/direction', 'w') as f:
		f.write(direction)

# Write value to GPIO pin 
def write_gpio(pin, value):
	with open(f'/sys/class/gpio/gpio{pin}/value', 'w') as f:
		f.write(str(value))

# Clean up and unexport the GPIO pin
def unexport_gpio(pin):
	with open('/sys/class/gpio/unexport', 'w') as f:
		f.write(str(pin))

# Function to list connected USB devices
def list_usb_devices():
	print("Connected USB Devices:")
	result = subprocess.run(['lsusb'], stdout=subprocess.PIPE)
	print(result.stdout.decode('utf-8'))

# Main program to control the GPIO pin and list USB devices:
	# Export and set up the GPIO pin
	export_gpio(GPIO_PIN)
	set_gpio_direction(GPIO_PIN, 'out')

	while True:
		# Turn the GPIO pin on (HIGH)
		write_gpio(GPIO_PIN, 1)
		list_usb_devices()  # List USB devices
		time.sleep(120)  # Wait for 120 second

		# Turn the GPIO pin off (LOW)
		write_gpio(GPIO_PIN, 0)
		list_usb_devices()  # List USB devices
		time.sleep(120)  # Wait for 120 second

except KeyboardInterrupt:

finally:
	# Clean up
	unexport_gpio(GPIO_PIN)
