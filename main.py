from fastapi import FastAPI,Header,Depends, HTTPException
from database import init_db
from models import MeetingRoom, Booking
from beanie import PydanticObjectId
from typing import Union
import jwt
import datetime
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
today = datetime.date.today()



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
# test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwicm9sZXMiOiJ1c2VyIn0.Y7eueui2xsh8rhVaa-nHjxestvcpJYEc8Y5qfU8HziM"
#to control all routes from dependency function
#to read multiple files from fast api documentation
#get the secret key from keycloak
#control route access in react for admin 
@app.on_event("startup")
async def start_db():
    await init_db()

async def token_check(token: Union[str,None]= Header(default=None)):
    print("this is token check function")
    if token==None:
        raise HTTPException(
            status_code=401,
            detail="You are not authorized as token is not included"
        )
    
    try:
        decoded_jwt = jwt.decode(token,options={"verify_signature": False})
        return decoded_jwt
    except:
        raise HTTPException(
            status_code=400,
            detail="We can't extract the informations since you didn't provid the correct token"

        )
    
async def get_role(role:dict=Depends(token_check)):
    print("This is get role function")
    usr_role = role['roles']
    return usr_role


#admin routes
@app.post('/creatroom')
async def CreateRoom(newRoom: MeetingRoom, ):
    await newRoom.create()
    return newRoom

@app.get('/getAllRooms')
async def GetAllRooms(token:str=Depends(get_role)):
    print(token)
    return await MeetingRoom.find().to_list()

@app.get('/getOneRoom/{roomId}')
async def GetOneRoom(roomId: PydanticObjectId, ):
    return await MeetingRoom.find_one(MeetingRoom.id ==roomId)

@app.put('/updateRoom/{roomId}')
async def UpdateRoom(roomId : PydanticObjectId, updateroom: MeetingRoom, ):
    room = await MeetingRoom.find_one(MeetingRoom.id == roomId)
    room.room_name = updateroom.room_name
    room.location = updateroom.location
    room.capacity = updateroom.capacity
    room.facilities = updateroom.facilities
    room.status = updateroom.status
    await room.save()
    return await MeetingRoom.find().to_list()

@app.delete('/deleteRoom/{roomId}')
async def DeleteRoom(roomId: PydanticObjectId, ):
    room = await MeetingRoom.find_one(MeetingRoom.id == roomId)
    await room.delete()
    return await MeetingRoom.find().to_list()


#booking routes
@app.post('/bookroom')
async def BookRoom(addBooking: Booking):
    bookedRoom = await MeetingRoom.find_one(MeetingRoom.id == addBooking.meeting_room)
    if addBooking.attendess > bookedRoom.capacity:
        raise HTTPException(
            status_code=401,
            detail="Attendess exceed the meeting room capacity"     
        )
    await addBooking.create()
    return addBooking   



@app.get('/getAllBooking')      
async def GetAllBooking():
    # import pdb
    # pdb.set_trace()
    todayandAfterBooks = []
    allBookings = await Booking.find().to_list()
    for booking in allBookings:
        if booking.booking_date >= datetime.datetime.now():
            todayandAfterBooks.append(booking)

    return todayandAfterBooks

@app.get('/getBookingsByRoomId/{roomId}')
async def GetBookingsByRoomId(roomId: PydanticObjectId):
    return await Booking.find(Booking.meeting_room == roomId).to_list()
