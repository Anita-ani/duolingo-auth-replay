from fastapi import FastAPI, Header, HTTPException
from database import users
from utils import get_user_id_from_token
from logger import log_access

app = FastAPI(title="Duolingo Replay – Secure Version")

@app.get("/user/profile")
def get_profile(authorization: str = Header(...)):
    user_id = get_user_id_from_token(authorization)

    if user_id is None or user_id not in users:
        log_access("invalid", "Blocked (unauthenticated)", "secure")
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = users[user_id]
    log_access(user.email, "Allowed", "secure")
    return user


@app.get("/logs")
def get_logs():
    try:
        with open("access.log", "r") as f:
            return {"logs": f.read().splitlines()[-20:]}  # last 20 entries
    except FileNotFoundError:
        return {"logs": []}
