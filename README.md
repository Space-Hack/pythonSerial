# Python Serial WebSocket Bridge

A Python application that bridges serial communication with WebSocket connections, allowing bidirectional data transfer between a serial device and a WebSocket server.

## Features

- Bidirectional communication between serial port and WebSocket server
- Real-time data transfer
- Error handling and graceful shutdown
- Thread-safe implementation

## Configuration

Before running the application, you may need to modify the following constants in `main.py`:

- `SERIAL_PORT`: The path to your serial device (default: '/dev/ttyACM1')
- `BAUD_RATE`: The baud rate for serial communication (default: 115200)
- `WEBSOCKET_URI`: The WebSocket server URI (default: "ws://168.119.174.209:8765")

## Usage

1. Connect your serial device to your computer
2. Run the application:
```bash
python main.py
```

The application will:
- Establish a connection to the WebSocket server
- Open the serial port
- Start two threads for bidirectional communication:
  - One thread reads from the serial port and sends data to the WebSocket
  - The other thread reads from the WebSocket and sends data to the serial port
