from typing import Optional
from pydantic import BaseModel

class ClerkPayload(BaseModel):
    user_id: str
    org_id: Optional[str] = None