# main.py
from datetime import datetime
from pydantic import Field
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from beanie import Document  # <-- We import Document here
from contextlib import asynccontextmanager
from typing import List

# 1. Import *only* the init_db function
from database import init_db

# --- 2. DEFINE THE MODEL DIRECTLY IN MAIN.PY ---
class SensorData(Document):
    x: float
    y: float
    z: float
    class Settings:
        name = "accelerometer_data"
# --- END OF MODEL DEFINITION ---


# --- Connection Manager (No Change) ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


# --- Input Model (No Change) ---
class SensorDataInput(BaseModel):
    x: float
    y: float
    z: float

    created_at: datetime = Field(default_factory=datetime.now) 

    class Settings:
        name = "accelerometer_data"
# --- 3. UPDATED LIFESPAN FUNCTION ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server starting up...")
    
    # We pass our list of models [SensorData] to the init function
    await init_db(models_list=[SensorData])
    
    print("Startup complete.")
    yield
    print("Server shutting down...")


# --- APP CREATION & CORS (No Change) ---
app = FastAPI(lifespan=lifespan)
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HOMEPAGE (No Change) ---
@app.get("/")
async def get_root_homepage():
    return {"message": "Hello, this is your first API!"}


# --- GET DATA (No Change) ---
# Our model is defined, so this works
@app.get("/data/accelerometer", response_model=List[SensorData])
async def get_accelerometer_data():
    data_points = await SensorData.find().sort("-$id").limit(100).to_list()
    return data_points


# --- POST DATA (No Change) ---
# Our model is defined, so this works
@app.post("/data/accelerometer", response_model=SensorData)
async def receive_accelerometer_data(
    data: SensorDataInput,
):
    db_sensor_data = SensorData(x=data.x, y=data.y, z=data.z)
    await db_sensor_data.insert()
    await manager.broadcast(db_sensor_data.model_dump_json())
    return db_sensor_data


# --- WEBSOCKET ENDPOINT (No Change) ---
@app.websocket("/ws/data")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("A client disconnected.")