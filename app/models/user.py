import datetime
import uuid


class UserPublic:
    id: uuid.UUID
    is_verified: bool
    created_at: datetime