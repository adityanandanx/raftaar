from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from config.settings import settings
from typing import Optional
import random
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_otp(length: int = 6) -> str:
    """Generate a random OTP"""
    return ''.join(random.choices(string.digits, k=length))


# Mock OTP storage (in production, store in Redis with TTL)
_otp_store = {}


def store_otp(phone: str, otp: str) -> None:
    """Store OTP for verification (mock implementation)"""
    _otp_store[phone] = {
        "otp": otp,
        "created_at": datetime.now(timezone.utc),
        "attempts": 0,
    }


def verify_otp(phone: str, otp: str) -> bool:
    """Verify OTP (mock implementation)"""
    if phone not in _otp_store:
        return False
    
    stored = _otp_store[phone]
    
    # Check if OTP expired (5 minutes)
    if datetime.now(timezone.utc) - stored["created_at"] > timedelta(minutes=5):
        del _otp_store[phone]
        return False
    
    # Check if too many attempts (3 attempts max)
    if stored["attempts"] >= 3:
        del _otp_store[phone]
        return False
    
    if stored["otp"] == otp:
        del _otp_store[phone]
        return True
    
    stored["attempts"] += 1
    return False
