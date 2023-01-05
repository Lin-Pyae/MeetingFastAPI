import motor.motor_asyncio
from beanie import init_beanie
from models import MeetingRoom, Booking


async def init_db():
    client =  motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.MeetingRoomBooking, document_models=[MeetingRoom, Booking])
    