import hmac, bcrypt

def verify_password(password: str, hashed_password: str) -> bool:
    """Securely verifies the user's password against the hash using bcrypt"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def verify_username(a: str | bytes, b: str | bytes) -> bool:
    """Compare's two strings or two bytes strings to prevent timing attacks"""
    return hmac.compare_digest(a, b)