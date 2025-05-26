# Duolingo Broken Authentication Replay

This project simulates a real-world API authentication flaw inspired by the Duolingo email-based scraping vulnerability. It includes both insecure and secure versions for demonstration and training purposes.

## 🔍 Real-World Context

The original bug allowed anyone to fetch user profile data without authentication by querying an email address.

---

## 🔓 Insecure App

| Endpoint                        | Method | Description                      |
|---------------------------------|--------|----------------------------------|
| `/public/user-info?email=`      | GET    | Exposes data without auth        |
| `/logs`                         | GET    | Shows access logs                |

Includes:
- No auth required
- Email enumeration
- Rate-limiting after 3 requests per 10s

---

## 🛡️ Secure App

| Endpoint           | Method | Description                           |
|--------------------|--------|---------------------------------------|
| `/user/profile`    | GET    | Requires token (e.g. `user-1`)        |
| `/logs`            | GET    | Shows access logs                     |

Fixes:
- Requires authentication
- No public email-based lookups

---

## 🚀 Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt

2. Run insecure app
cd insecure_app
uvicorn main:app --reload --port 8010

3. Run secure app
cd ../secure_app
uvicorn main:app --reload --port 8011

4. Test
# Insecure - works without login
curl "http://127.0.0.1:8010/public/user-info?email=anita@duolingo.com"

# Secure - needs valid token
curl "http://127.0.0.1:8011/user/profile" -H "authorization: user-1"


 Educational Use Only
This project is for training and demo purposes. Do not use it in production.
