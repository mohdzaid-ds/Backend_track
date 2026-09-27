
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth import get_current_user
from supabase_client import supabase

app = FastAPI()

# Bearer token security for Swagger UI
security = HTTPBearer()


# 1. ROOT

@app.get("/")
def root():
    return {
        "message": "FastAPI is connected to Supabase"
    }


# 2. TEST SUPABASE CONNECTION

@app.get("/test-supabase")
def test_supabase():
    try:
        response = supabase.table("tasks").select("*").execute()

        return {
            "message": "Supabase connection successful",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# 3. SIGN UP

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(email: str, password: str):

    # Validate input
    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        return {
            "message": "Signup successful",
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# 4. LOGIN


@app.post("/auth/login")
def login(email: str, password: str):

    # Validate input
    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        return {
            "message": "Login successful",
            "user": response.user,
            "session": response.session
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )


# 5. PUBLIC INFORMATION

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public.",
        "authentication_required": False
    }


# 6. PROTECTED PROFILE

@app.get("/protected/profile")
def profile(user=Depends(get_current_user)):

    return {
        "message": "Profile accessed successfully",
        "user_id": user.get("sub"),
        "email": user.get("email")
    }



# 7. PROTECTED DASHBOARD

@app.get("/protected/dashboard")
def dashboard(user=Depends(get_current_user)):

    return {
        "message": "Dashboard accessed successfully",
        "user_id": user.get("sub"),
        "email": user.get("email")
    }


# 8. LOGOUT

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user=Depends(get_current_user)):

    try:
        supabase.auth.sign_out()

        # 204 responses should not contain a response body
        return None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
