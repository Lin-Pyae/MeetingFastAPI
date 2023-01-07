from beanie import Document,PydanticObjectId, Link
from typing import List, Optional
from datetime import datetime

class MeetingRoom(Document):
    room_name: str
    location: str
    capacity: int
    facilities: List[str]
    status: Optional[bool] = False

    class Settings:
        name = "Meeting Rooms"


class Booking(Document):
    meeting_room: Link[MeetingRoom]
    meeting_title: str
    attendess: List[str]
    start_time: datetime
    end_time: datetime
    booking_date: datetime

    class Settings:
        name = "Bookings"
