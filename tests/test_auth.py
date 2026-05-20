"""Tests for authentication module"""
import pytest
from fastapi import status


class TestUserRegistration:
    """Test user registration endpoint"""
    
    def test_register_new_user_success(self, client):
        """Test successful user registration"""
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe",
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["access_token"]
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["phone"] == "9876543210"
        assert data["user"]["first_name"] == "John"
        assert data["user"]["role"] == "customer"
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # Register first user
        client.post("/auth/register", json={
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "securepassword123",
        })
        
        # Try to register with same email
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "phone": "9876543211",
            "password": "securepassword123",
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]
    
    def test_register_duplicate_phone(self, client):
        """Test registration with duplicate phone"""
        # Register first user
        client.post("/auth/register", json={
            "email": "test1@example.com",
            "phone": "9876543210",
            "password": "securepassword123",
        })
        
        # Try to register with same phone
        response = client.post("/auth/register", json={
            "email": "test2@example.com",
            "phone": "9876543210",
            "password": "securepassword123",
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post("/auth/register", json={
            "email": "invalid-email",
            "phone": "9876543210",
            "password": "securepassword123",
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_short_password(self, client):
        """Test registration with password too short"""
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "short",
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserLogin:
    """Test user login endpoint"""
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user first
        client.post("/auth/register", json={
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "securepassword123",
        })
        
        # Login
        response = client.post("/auth/login?email=test@example.com&password=securepassword123")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["access_token"]
        assert data["user"]["email"] == "test@example.com"
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        # Register user
        client.post("/auth/register", json={
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "securepassword123",
        })
        
        # Try wrong password
        response = client.post("/auth/login?email=test@example.com&password=wrongpassword")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post("/auth/login?email=nonexistent@example.com&password=password123")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetCurrentUser:
    """Test get current user endpoint"""
    
    def test_get_me_success(self, client):
        """Test getting current user profile"""
        # Register and login
        register_response = client.post("/auth/register", json={
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "securepassword123",
            "first_name": "John",
        })
        token = register_response.json()["access_token"]
        
        # Get current user
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "John"
    
    def test_get_me_without_token(self, client):
        """Test getting current user without token"""
        response = client.get("/auth/me")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_me_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateProfile:
    """Test update profile endpoint"""
    
    def test_update_profile_success(self, client):
        """Test successful profile update"""
        # Register user
        register_response = client.post("/auth/register", json={
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "securepassword123",
            "first_name": "John",
        })
        token = register_response.json()["access_token"]
        
        # Update profile
        response = client.put(
            "/auth/profile",
            json={
                "first_name": "Jane",
                "last_name": "Smith",
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == "Jane"
        assert data["last_name"] == "Smith"
    
    def test_update_email_to_existing(self, client):
        """Test updating email to one that already exists"""
        # Register two users
        client.post("/auth/register", json={
            "email": "test1@example.com",
            "phone": "9876543210",
            "password": "password123",
        })
        
        register_response = client.post("/auth/register", json={
            "email": "test2@example.com",
            "phone": "9876543211",
            "password": "password123",
        })
        token = register_response.json()["access_token"]
        
        # Try to update email to existing one
        response = client.put(
            "/auth/profile",
            json={"email": "test1@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already in use" in response.json()["detail"]


class TestOTP:
    """Test OTP functionality"""
    
    def test_send_otp_success(self, client):
        """Test successful OTP sending"""
        response = client.post("/auth/send-otp", json={
            "phone": "9876543210"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "OTP sent to phone"
        assert data["phone"] == "9876543210"
    
    def test_verify_otp_success(self, client):
        """Test successful OTP verification"""
        # Send OTP
        send_response = client.post("/auth/send-otp", json={
            "phone": "9876543210"
        })
        otp = send_response.json()["otp"]
        
        # Verify OTP
        response = client.post("/auth/verify-otp", json={
            "phone": "9876543210",
            "otp": otp
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["verified"] is True
    
    def test_verify_otp_invalid(self, client):
        """Test OTP verification with wrong code"""
        # Send OTP
        client.post("/auth/send-otp", json={
            "phone": "9876543210"
        })
        
        # Try wrong OTP
        response = client.post("/auth/verify-otp", json={
            "phone": "9876543210",
            "otp": "000000"
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid or expired OTP" in response.json()["detail"]
