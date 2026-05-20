from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import (
    UserCreate, UserResponse, TokenResponse, OTPRequest, OTPVerify, UserUpdate
)
from app.services.auth_service import (
    hash_password, verify_password, create_access_token, decode_token,
    generate_otp, store_otp, verify_otp
)
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    
    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    existing_phone = db.query(User).filter(User.phone == user_create.phone).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )
    
    # Create new user
    user = User(
        email=user_create.email,
        phone=user_create.phone,
        hashed_password=hash_password(user_create.password),
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        role=UserRole.CUSTOMER,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    logger.info(f"New user registered: {user.id} - {user.email}")
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login user with email and password"""
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    logger.info(f"User login: {user.id} - {user.email}")
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(user),
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's profile"""
    return UserResponse.from_orm(current_user)


@router.put("/profile", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user profile"""
    # Check if email is being changed and already exists
    if user_update.email and user_update.email != current_user.email:
        existing = db.query(User).filter(User.email == user_update.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use",
            )
        current_user.email = user_update.email
    
    # Check if phone is being changed and already exists
    if user_update.phone and user_update.phone != current_user.phone:
        existing = db.query(User).filter(User.phone == user_update.phone).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already in use",
            )
        current_user.phone = user_update.phone
    
    if user_update.first_name is not None:
        current_user.first_name = user_update.first_name
    
    if user_update.last_name is not None:
        current_user.last_name = user_update.last_name
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"User profile updated: {current_user.id}")
    
    return UserResponse.from_orm(current_user)


@router.post("/send-otp")
def send_otp(otp_request: OTPRequest):
    """Send OTP to phone number (mock implementation)"""
    otp = generate_otp()
    store_otp(otp_request.phone, otp)
    
    # In production, send via SMS provider
    logger.info(f"OTP generated for {otp_request.phone}: {otp}")
    
    return {
        "message": "OTP sent to phone",
        "phone": otp_request.phone,
        # For testing purposes only - remove in production
        "otp": otp if True else None,  # Set False in production
    }


@router.post("/verify-otp", response_model=dict)
def verify_otp_endpoint(otp_verify: OTPVerify):
    """Verify OTP sent to phone"""
    if verify_otp(otp_verify.phone, otp_verify.otp):
        return {
            "verified": True,
            "message": "OTP verified successfully",
        }
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired OTP",
    )
