from enum import Enum

class UserType(str, Enum):
    TENANT = "Tenant"
    LANDLORD = "Landlord"

    @classmethod
    def choices(cls):
        return [(role.value, role.value) for role in cls]
