from fastapi import FastAPI, Request, Query
from database import users
from logger import log_access
import time

app = FastAPI(title="Duolingo Replay – Insecure Version")

# Simple in-memory rate limiter
rate_limit_tracker = {}

@app.get("/public/user-info")
def get_user_info(request: Request, email: str = Query(...)):
    ip = request.client.host
    now = time.time()

    # Track recent requests per IP
    access_log = rate_limit_tracker.get(ip, [])
    access_log = [ts for ts in access_log if now - ts < 10]  # last 10 seconds

    if len(access_log) >= 3:
        log_access(email, "Blocked (rate limited)", "insecure")
        return {"detail": "Too many requests. Please slow down."}

    access_log.append(now)
    rate_limit_tracker[ip] = access_log

    # Email lookup
    user = next((u for u in users.values() if u.email == email), None)

    if user:
        log_access(email, "Allowed", "insecure")
        return user
    else:
        log_access(email, "Blocked (not found)", "insecure")
        return {"detail": "User not found"}


@app.get("/logs")
def get_logs():
    try:
        with open("access.log", "r") as f:
            return {"logs": f.read().splitlines()[-20:]}  # Last 20 entries
    except FileNotFoundError:
        return {"logs": []}


@app.get("/logs")
def get_logs():
    try:
        with open("access.log", "r") as f:
            return {"logs": f.read().splitlines()[-20:]}  # last 20 entries
    except FileNotFoundError:
        return {"logs": []}
