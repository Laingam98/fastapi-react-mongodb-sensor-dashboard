# FastAPI React MongoDB Sensor Dashboard

A full-stack, real-time sensor dashboard. This project streams live accelerometer data from an STBL4S5I IoT board to a MongoDB database and visualizes it live using React, Chart.js, and WebSockets.

---

## Features

* **Real-time Data:** Live data streaming from hardware to the browser using WebSockets.
* **NoSQL Database:** Uses MongoDB to store high-volume time-series data efficiently.
* **Modern Frontend:** A clean, responsive dashboard built with React and Chart.js.
* **Async Backend:** Built with FastAPI and Beanie for high-performance, asynchronous database operations.

---

## Tech Stack

* **Backend:** Python, FastAPI, MongoDB, Beanie (ODM), WebSockets
* **Frontend:** React.js, Chart.js, JavaScript (ES6+), CSS
* **Hardware:** STBL4S5I IoT Board (LSM6DSL sensor)
* **Bridge:** A `pyserial` script to translate UART to HTTP.

---

## How It Works (Data Pipeline)

1.  The **ST Board** reads sensor data and sends it over UART.
2.  A **Python Bridge (`bridge.py`)** listens to the serial port, parses the data, and `POST`s it to the API.
3.  The **FastAPI Server (`main.py`)** saves the data to **MongoDB** and instantly **broadcasts** it via **WebSockets**.
4.  The **React Dashboard (`App.js`)** receives the WebSocket message and updates the chart and table in real-time.

---

## How to Run

### 1. Backend (`my_first_backened`)

* You must have **MongoDB Server** installed and running locally.

```bash
# 1. Go into the backend folder
cd my_first_backened

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server
uvicorn main:app --reload
```

### 2. Terminal 2: Run the Frontend Dashboard
* You must have Node.js installed.
* This is a second, separate terminal.

```bash
# 1. Go into the frontend folder
cd sensor-dashboard

# 2. Install all node dependencies (only needed the first time)
npm install

# 3. Run the development server
npm start
```

### 3. Terminal 3: Run the Bridge (to start the data)
* Plug in your ST Board.
* This is a third, separate terminal.

```bash
# 1. Go into the backened folder
cd my_first_backened

# 2. Activate the virtual environment
.\venv\Scripts\activate

# 3. IMPORTANT: You must update the SERIAL_PORT
#    variable inside the 'bridge.py' file to match your COM port.

# 4. Run the bridge script.
python bridge.py



  

