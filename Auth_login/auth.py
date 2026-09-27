
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from supabase_client import supabase


security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    token = credentials.credentials
    print("TOKEN RECEIVED:", token[:20])

    try:
        response = supabase.auth.get_user(token)

        user = getattr(response, "user", None)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return {
            "sub": user.id,
            "email": user.email
        }

    except HTTPException:
        raise

    except Exception as e:
        print("AUTH ERROR:", type(e).__name__, str(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )