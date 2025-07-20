def get_user_id_from_token(token: str) -> int:
    try:
        return int(token.split("-")[1])  # e.g., "user-1"
    except:
        return None
