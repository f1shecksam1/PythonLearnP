from fastapi import APIRouter, HTTPException, status

from learnpyapp.core.security import create_access_token, hash_password, verify_password
from learnpyapp.schemas.auth import LoginRequest, Token

router = APIRouter(tags=["auth"])

# 🧪 Şimdilik fake user (DB gelince burası değişecek)
FAKE_USER = {
    "email": "admin@example.com",
    "hashed_password": hash_password("secret"),
}


@router.post("/login", response_model=Token)
def login(data: LoginRequest) -> Token:
    if data.email != FAKE_USER["email"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not verify_password(data.password, FAKE_USER["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = create_access_token({"sub": data.email})

    return Token(access_token=token)
