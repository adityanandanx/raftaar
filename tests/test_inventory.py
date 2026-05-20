"""Tests for bike and station inventory management"""
import pytest
from fastapi import status


def create_admin_user(client):
    """Helper to create admin user"""
    response = client.post("/auth/register", json={
        "email": "admin@example.com",
        "phone": "9876543210",
        "password": "adminpassword123",
    })
    return response.json()["access_token"]


def create_customer_user(client):
    """Helper to create customer user"""
    response = client.post("/auth/register", json={
        "email": "customer@example.com",
        "phone": "9876543211",
        "password": "customerpassword123",
    })
    return response.json()["access_token"]


class TestStationManagement:
    """Test station management endpoints"""
    
    def test_create_station_as_admin(self, client):
        """Test creating station as admin"""
        admin_token = create_admin_user(client)
        
        response = client.post(
            "/admin/stations",
            json={
                "name": "Central Station",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Central Station"
        assert data["latitude"] == 28.6139
        assert data["longitude"] == 77.2090
        assert data["capacity"] == 20
    
    def test_create_station_as_customer_fails(self, client):
        """Test that customer cannot create station"""
        customer_token = create_customer_user(client)
        
        response = client.post(
            "/admin/stations",
            json={
                "name": "Central Station",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {customer_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Admin access required" in response.json()["detail"]
    
    def test_create_station_invalid_coordinates(self, client):
        """Test creating station with invalid coordinates"""
        admin_token = create_admin_user(client)
        
        # Invalid latitude
        response = client.post(
            "/admin/stations",
            json={
                "name": "Invalid Station",
                "latitude": 95.0,  # > 90
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_all_stations(self, client):
        """Test getting all stations"""
        admin_token = create_admin_user(client)
        
        # Create 2 stations
        for i in range(2):
            client.post(
                "/admin/stations",
                json={
                    "name": f"Station {i+1}",
                    "latitude": 28.6139 + i,
                    "longitude": 77.2090 + i,
                    "capacity": 20,
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )
        
        response = client.get(
            "/admin/stations",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 2
    
    def test_update_station(self, client):
        """Test updating a station"""
        admin_token = create_admin_user(client)
        
        # Create station
        create_response = client.post(
            "/admin/stations",
            json={
                "name": "Original Name",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        station_id = create_response.json()["id"]
        
        # Update station
        response = client.put(
            f"/admin/stations/{station_id}",
            json={
                "name": "Updated Name",
                "capacity": 30,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["capacity"] == 30


class TestBikeManagement:
    """Test bike management endpoints"""
    
    def test_add_bike_to_station(self, client):
        """Test adding bike to station"""
        admin_token = create_admin_user(client)
        
        # Create station first
        station_response = client.post(
            "/admin/stations",
            json={
                "name": "Test Station",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        station_id = station_response.json()["id"]
        
        # Add bike
        response = client.post(
            "/admin/bikes",
            json={
                "station_id": station_id,
                "qr_code_hash": "qr_hash_12345",
                "model": "Mountain Bike",
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["qr_code_hash"] == "qr_hash_12345"
        assert data["model"] == "Mountain Bike"
        assert data["status"] == "available"
    
    def test_add_bike_duplicate_qr_code(self, client):
        """Test adding bike with duplicate QR code"""
        admin_token = create_admin_user(client)
        
        # Create station
        station_response = client.post(
            "/admin/stations",
            json={
                "name": "Test Station",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        station_id = station_response.json()["id"]
        
        # Add first bike
        client.post(
            "/admin/bikes",
            json={
                "station_id": station_id,
                "qr_code_hash": "qr_hash_12345",
                "model": "Mountain Bike",
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        # Try to add duplicate
        response = client.post(
            "/admin/bikes",
            json={
                "station_id": station_id,
                "qr_code_hash": "qr_hash_12345",
                "model": "Road Bike",
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "QR code already exists" in response.json()["detail"]
    
    def test_add_bike_invalid_station(self, client):
        """Test adding bike to non-existent station"""
        admin_token = create_admin_user(client)
        
        response = client.post(
            "/admin/bikes",
            json={
                "station_id": 99999,
                "qr_code_hash": "qr_hash_12345",
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Station not found" in response.json()["detail"]
    
    def test_mark_bike_maintenance(self, client):
        """Test marking bike for maintenance"""
        admin_token = create_admin_user(client)
        
        # Create station and bike
        station_response = client.post(
            "/admin/stations",
            json={
                "name": "Test Station",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        station_id = station_response.json()["id"]
        
        bike_response = client.post(
            "/admin/bikes",
            json={
                "station_id": station_id,
                "qr_code_hash": "qr_hash_12345",
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        bike_id = bike_response.json()["id"]
        
        # Mark for maintenance
        response = client.put(
            f"/admin/bikes/{bike_id}/maintenance",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "maintenance"
    
    def test_retire_bike(self, client):
        """Test retiring a bike"""
        admin_token = create_admin_user(client)
        
        # Create station and bike
        station_response = client.post(
            "/admin/stations",
            json={
                "name": "Test Station",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        station_id = station_response.json()["id"]
        
        bike_response = client.post(
            "/admin/bikes",
            json={
                "station_id": station_id,
                "qr_code_hash": "qr_hash_12345",
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        bike_id = bike_response.json()["id"]
        
        # Retire bike
        response = client.put(
            f"/admin/bikes/{bike_id}/retire",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "retired"
        assert data["is_active"] is False
    
    def test_get_all_bikes(self, client):
        """Test getting all bikes"""
        admin_token = create_admin_user(client)
        
        # Create station and add bikes
        station_response = client.post(
            "/admin/stations",
            json={
                "name": "Test Station",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 20,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        station_id = station_response.json()["id"]
        
        for i in range(3):
            client.post(
                "/admin/bikes",
                json={
                    "station_id": station_id,
                    "qr_code_hash": f"qr_hash_{i}",
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )
        
        response = client.get(
            "/admin/bikes",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 3
    
    def test_get_low_availability_stations(self, client):
        """Test getting stations with low availability"""
        admin_token = create_admin_user(client)
        
        # Create station with limited bikes
        station_response = client.post(
            "/admin/stations",
            json={
                "name": "Low Availability Station",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "capacity": 5,
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        station_id = station_response.json()["id"]
        
        # Add only 1 bike (4 empty slots)
        client.post(
            "/admin/bikes",
            json={
                "station_id": station_id,
                "qr_code_hash": "qr_hash_single",
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        response = client.get(
            "/admin/stations/low-availability",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
