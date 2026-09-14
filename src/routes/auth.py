from fastapi import APIRouter,Depends
from ..services.auth import get_or_create_user_and_org


router = APIRouter(prefix="/auth",tags=["auth"])

@router.get("/current-user")
async def get_current_user(payload=Depends(get_or_create_user_and_org)):
    user, org = payload
    return {
        "user_id": str(user.id),
        "clerk_user_id": user.clerk_user_id,
        "org_id": org.clerk_org_id if org else None,
    }
