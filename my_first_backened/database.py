# database.py
import motor.motor_asyncio
from beanie import init_beanie

# This function is now simpler. It just connects
# and initializes whatever models we pass to it.
async def init_db(models_list):
    
    # 1. Connect to the MongoDB server
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017"
    )
    
    # 2. Get the database
    db = client.my_sensor_db

    # 3. Initialize beanie with the models passed from main.py
    await init_beanie(database=db, document_models=models_list)
    
    print("Beanie (MongoDB) initialized successfully.")