from enum import Enum

class LeaveStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"

    
class LeaveType(str, Enum):
    SICK = "SICK"
    CASUAL = "CASUAL"    