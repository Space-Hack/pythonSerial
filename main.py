import serial
import time
import threading
from websockets.sync.client import connect, ClientConnection

# SERIAL_PORT = '/dev/ttyACM1'
SERIAL_PORT = '/dev/tty.usbmodem2103'
BAUD_RATE = 115200
WEBSOCKET_URI = "ws://localhost:8765"


def read_from_serial(ser: serial.Serial, websocket: ClientConnection):
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').rstrip()
                print(f"Serial → WS: {line}")
                websocket.send(line)
            except Exception as e:
                print(f"WebSocket read error: {e}")
                break
            time.sleep(0.01)


def read_from_websocket(ser: serial.Serial, websocket: ClientConnection):
    while True:
        try:
            message = websocket.recv()
            print(f"WS → Serial: {message}")
            ser.write((message + '\n').encode('utf-8'))
        except Exception as e:
            print(f"WebSocket read error: {e}")
            break
        time.sleep(0.01)


def start_socket():
    try:
        with connect(WEBSOCKET_URI) as websocket:
            name = input("What's your name? ")
            websocket.send(name)
            print(f">>> {name}")
            greeting = websocket.recv()
            print(f"<<< {greeting}")

            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"Connected to {ser.name}")

            # Start serial to websocket thread
            serial_thread = threading.Thread(
                target=read_from_serial, args=(ser, websocket), daemon=True)
            serial_thread.start()

            # Main thread handles websocket to serial
            read_from_websocket(ser, websocket)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    # ser.write(("FORWARD:100.0" + '\n').encode('utf-8'))
    # time.sleep(2)
    # ser.write(("BACKWARD:10.0" + '\n').encode('utf-8'))
    # ser.write(("TURN:10.0" + '\n').encode('utf-8'))
    # ser.write(("STOP" + '\n').rencode('utf-8'))