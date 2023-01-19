from beanie import Document,PydanticObjectId, Link
from typing import List, Optional
from datetime import date, datetime

today = datetime.today().date()
class MeetingRoom(Document):
    room_name: str
    location: str
    capacity: int
    facilities: List[str]
    status: Optional[bool] = False

    class Settings:
        name = "meeting_rooms"


class Booking(Document):
    meeting_room: PydanticObjectId
    meeting_title: str
    attendess: int
    start_time: int
    end_time: int
    booking_date: str

    class Settings:
        name = "bookings_db"