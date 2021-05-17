from enum import Enum


class PresenceEvent(Enum):
    PRESENT = 'PRESENT'
    NOT_PRESENT = 'NOT_PRESENT'
    # NOT_AVAILABLE is used in case the camera is not available,
    # in this case it's possible that since the camera is in use the user is present
    NOT_AVAILABLE = 'NOT_AVAILABLE'
