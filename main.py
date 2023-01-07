from fastapi import FastAPI,Header,Depends, HTTPException
from database import init_db
from models import MeetingRoom, Booking
from beanie import PydanticObjectId
from typing import Union
import jwt

app = FastAPI()

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
async def CreateRoom(newRoom: MeetingRoom):
    await newRoom.create()
    return newRoom

@app.get('/getAllRooms')
async def GetAllRooms(token:str=Depends(get_role)):
    print(token)
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

@app.delete('/deleteRoom/{roomId}')
async def DeleteRoom(roomId: PydanticObjectId):
    room = await MeetingRoom.find_one(MeetingRoom.id == roomId)
    await room.delete()
    return {f"Successfully deleted room {room.room_name}"}


#booking routes
@app.post('/bookroom')
async def BookRoom(addBooking: Booking):
    import pdb
    pdb.set_trace()
    # print("This is id ",type(addBooking.meeting_room))
    roomId = PydanticObjectId(addBooking.meeting_room)
    print(type(roomId))
    room = await MeetingRoom.find_one(MeetingRoom.id == roomId)
    print(room)
    room.status = True
    await room.save()
    # addBooking.meeting_room["_id"] = room.id
    # addBooking.meeting_room["room_name"] = room.room_name
    # addBooking.meeting_room["location"] = room.location
    # addBooking.meeting_room["capacity"] = room.capacity
    # addBooking.meeting_room["facilities"] = room.facilities
    # addBooking.meeting_room["status"] = True
    addBooking.meeting_room = room
    await addBooking.create()
    return addBooking