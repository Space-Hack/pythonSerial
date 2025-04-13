import serial
import time

# Replace with the actual port identified in step 3
SERIAL_PORT = '/dev/ttyACM1'
# Baud rate might not be strictly necessary for USB CDC,
# but 115200 is a common default if issues arise.
BAUD_RATE = 115200

try:
    # timeout=1 means ser.readline() will wait up to 1 second for data
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {ser.name}")

    while True:
        # Read one line of text, decode from bytes to string, remove whitespace
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Received: {line}")
        # Optional: add a small delay to prevent busy-waiting
        # time.sleep(0.01)

except serial.SerialException as e:
    print(f"Error opening or reading from serial port: {e}")
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")