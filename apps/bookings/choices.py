from enum import Enum


class BookingStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    DECLINED = "Declined"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


    @classmethod
    def choices(cls):
        return [(status.value, status.value) for status in cls]


