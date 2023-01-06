from fastapi import FastAPI
from database import init_db
from models import MeetingRoom, Booking
from beanie import PydanticObjectId

app = FastAPI()

@app.on_event("startup")
async def start_db():
    await init_db()

# @app.on_event("shutdown")
# async def shutdown_db():
#     print("database has shut down")


@app.post('/creatroom')
async def CreateRoom(newRoom: MeetingRoom):
    await newRoom.create()
    return newRoom


@app.get('/getAllRooms')
async def GetAllRooms():
    return await MeetingRoom.find().to_list()

@app.put('/updateRoom/{roomId}')
async def UpdateRoom(roomId : PydanticObjectId, updateroom: MeetingRoom):
    room = await MeetingRoom.find_one(MeetingRoom.id == roomId)
    room.room_name = updateroom.room_name
    room.location = updateroom.location
    room.capacity = updateroom.capacity
    room.facilities = updateroom.facilities
    await room.save()
    return room


