from enum import Enum


class PropertyType(str, Enum):
    APARTMENT = "Apartment"
    HOUSE = "House"
    STUDIO = "Studio"
    ROOM = "Room"
    LOFT = "Loft"
    PENTHOUSE = "Penthouse"
    BUNGALOW = "Bungalow"
    VILLA = "Villa"
    TINY_HOUSE = "Tiny House"
    MOBILE_HOME = "Mobile Home"


    @classmethod
    def choices(cls):
        return [(type.value, type.value) for type in cls]

