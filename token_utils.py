import os
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


_SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
_TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "86400"))
_SERIALIZER = URLSafeTimedSerializer(_SECRET_KEY, salt="auth-token")


def generate_token(user_id):
    return _SERIALIZER.dumps({"user_id": user_id})


def verify_token(token):
    try:
        return _SERIALIZER.loads(token, max_age=_TOKEN_TTL_SECONDS)
    except (SignatureExpired, BadSignature):
        return None


def extract_token_from_request(request):
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()

    return request.headers.get("X-Access-Token")
