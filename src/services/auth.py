from fastapi import Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from ..core.config import settings
from ..schema.utils import ClerkPayload
from ..core.db import db_dependency,User,Organization
from sqlalchemy import select
import jwt


security = HTTPBearer()
jwt_client = jwt.PyJWKClient(settings.CLERK_JWKS_URL)


def verify_token(crediential: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = crediential.credentials
        signing_key = jwt_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(token, signing_key.key, algorithms=["RS256"], options={"verify_aud": False}, leeway=60)
        user_id = payload.get("sub")
        org_id = payload.get("org_id")
        return ClerkPayload(user_id=user_id, org_id=org_id)
    except jwt.ExpiredSignatureError as e:
        print("Token verification expired:", e)
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        print("Token verification invalid:", e)
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print("Unexpected error in token verification:", e)
        raise HTTPException(status_code=401, detail=str(e))



async def get_or_create_user_and_org(db:db_dependency,payload: ClerkPayload = Depends(verify_token)):
    result  = await db.execute(select(User).where(User.clerk_user_id == payload.user_id))
    user = result.scalar_one_or_none()
    if not user:
        print("User Not Found Creating it...")
        user = User(clerk_user_id=payload.user_id)
        db.add(user)
        await db.flush()
        
    org = None
    if payload.org_id:
        result  = await db.execute(select(Organization).where(Organization.clerk_org_id == payload.org_id))
        org = result.scalar_one_or_none()
        if not org:
            print("Org not Found Creating One...")
            org = Organization(clerk_org_id=payload.org_id, owner_id=user.id)
            db.add(org)
            await db.flush()
    else:
        # Fallback to user's first organization if exists
        result = await db.execute(select(Organization).where(Organization.owner_id == user.id))
        org = result.scalar_one_or_none()
        
    await db.commit()
    return user,org
    