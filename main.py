from fastapi import FastAPI,Header,Depends, HTTPException
from database import init_db
from models import MeetingRoom, Booking
from beanie import PydanticObjectId
from typing import Union
import jwt
import datetime
from fastapi.middleware.cors import CORSMiddleware
from auth import admin,user
import pytz

app = FastAPI()
today = datetime.date.today()
myanmar_tz = pytz.timezone("Asia/Rangoon")


origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_db():
    await init_db()



#admin routes
@app.post('/createRoom')
async def CreateRoom(newRoom: MeetingRoom, token:str=Depends(admin)):
    await newRoom.create()
    return newRoom

@app.get('/getAllRooms')
async def GetAllRooms(token:str=Depends(user)):
    # print(token)
    return await MeetingRoom.find().to_list()

@app.get('/getOneRoom/{roomId}')
async def GetOneRoom(roomId: PydanticObjectId, token:str=Depends(admin)):
    return await MeetingRoom.find_one(MeetingRoom.id ==roomId)

@app.put('/updateRoom/{roomId}')
async def UpdateRoom(roomId : PydanticObjectId, updateroom: MeetingRoom, token:str=Depends(admin)):
    room = await MeetingRoom.find_one(MeetingRoom.id == roomId)
    room.room_name = updateroom.room_name
    room.location = updateroom.location
    room.capacity = updateroom.capacity
    room.facilities = updateroom.facilities
    room.status = updateroom.status
    await room.save()
    return await MeetingRoom.find().to_list()

@app.delete('/deleteRoom/{roomId}')
async def DeleteRoom(roomId: PydanticObjectId, token:str=Depends(admin)):
    room = await MeetingRoom.find_one(MeetingRoom.id == roomId)
    await room.delete()
    return await MeetingRoom.find().to_list()


#booking routes
@app.post('/bookroom')
async def BookRoom(addBooking: Booking, token:str=Depends(user)):
    bookedRoom = await MeetingRoom.find_one(MeetingRoom.id == addBooking.meeting_room)
    allBookings = await Booking.find().to_list()
    if addBooking.attendess > bookedRoom.capacity:
        return "exceed"

    for booking in allBookings:
        if booking.meeting_room == addBooking.meeting_room:
            if (booking.start_time <= addBooking.start_time  <= booking.end_time) :
                return False
    await addBooking.create()
    return addBooking   



@app.get('/getAllBooking')      
async def GetAllBooking(token:str=Depends(user)):
    todayandAfterBooks = []
    allBookings = await Booking.find().to_list()
    for booking in allBookings:
        if booking.end_time >= datetime.datetime.now():
            todayandAfterBooks.append(booking)

    return todayandAfterBooks

@app.get('/getBookingsByRoomId/{roomId}')
async def GetBookingsByRoomId(roomId: PydanticObjectId, token:str=Depends(user)):
    
    return await Booking.find(Booking.meeting_room == roomId).to_list()