from beanie import Document
from typing import List
from datetime import datetime

class MeetingRoom(Document):
    room_name: str
    location: str
    capacity: int
    facilities: List[str]

    class Settings:
        name = "Meeting Rooms"


class Booking(Document):
    meeting_title: str
    attendess: int
    meeting_room: str
    start_time: datetime
    end_time: datetime
    booking_date: datetime

    class Settings:
        name = "Bookings"
