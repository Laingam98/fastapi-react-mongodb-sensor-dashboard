import serial
import requests
import time

SERIAL_PORT = 'COM16'  

BAUD_RATE = 115200

API_ENDPOINT = "http://127.0.0.1:8000/data/accelerometer"

print("--- Starting UART-to-HTTP Bridge ---")
print(f"Listening on: {SERIAL_PORT} @ {BAUD_RATE} bps")
print(f"Forwarding to: {API_ENDPOINT}")

def run_bridge():
    while True:
        try:
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
                print(f"Serial port {SERIAL_PORT} opened successfully.")

                while True:
                    line_bytes = ser.readline()
                    if not line_bytes:
                        continue
                    line_str = line_bytes.decode('utf-8').strip()
                    try:
                        parts = line_str.split(',')
                        if len(parts) == 3:
                            x = float(parts[0])
                            y = float(parts[1])
                            z = float(parts[2])
                            payload = {
                                "x": x,
                                "y": y,
                                "z": z
                            }
                            response = requests.post(API_ENDPOINT, json=payload)

                            if response.status_code == 200:
                                print(f"Sent: {payload} -> Response: OK (200)")
                            else:
                                print(f"Sent: {payload} -> Error: {response.status_code}")

                        else:
                            print(f"Skipping malformed line: {line_str}")

                    except ValueError:
                        print(f"Could not parse line to float: {line_str}")
                    except requests.exceptions.ConnectionError:
                        print(f"Error: Connection to {API_ENDPOINT} failed. Is main.py running?")
                        time.sleep(2) 

        except serial.SerialException as e:
            print(f"Error: Could not open serial port {SERIAL_PORT}.")
            print("  1. Is the board plugged in?")
            print(f"  2. Is {SERIAL_PORT} the correct port?")
            print("  3. Is no other program (like CubeMonitor) using it?")
            print(f"Retrying in 5 seconds... (Error details: {e})")
            time.sleep(5)

if __name__ == "__main__":
    run_bridge()