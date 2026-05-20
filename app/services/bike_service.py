"""Service functions for bike and station management"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.bike import Bike, Station, BikeStatus
from typing import List, Optional


def get_station_by_id(db: Session, station_id: int) -> Optional[Station]:
    """Get station by ID"""
    return db.query(Station).filter(Station.id == station_id).first()


def get_all_stations(db: Session, skip: int = 0, limit: int = 100) -> List[Station]:
    """Get all stations with pagination"""
    return db.query(Station).offset(skip).limit(limit).all()


def create_station(
    db: Session,
    name: str,
    latitude: float,
    longitude: float,
    capacity: int,
) -> Station:
    """Create a new station"""
    station = Station(
        name=name,
        latitude=latitude,
        longitude=longitude,
        capacity=capacity,
    )
    db.add(station)
    db.commit()
    db.refresh(station)
    return station


def update_station(
    db: Session,
    station_id: int,
    name: Optional[str] = None,
    capacity: Optional[int] = None,
) -> Optional[Station]:
    """Update a station"""
    station = get_station_by_id(db, station_id)
    if not station:
        return None
    
    if name is not None:
        station.name = name
    if capacity is not None:
        station.capacity = capacity
    
    db.commit()
    db.refresh(station)
    return station


def get_bikes_by_station(db: Session, station_id: int) -> List[Bike]:
    """Get all bikes for a station"""
    return db.query(Bike).filter(Bike.station_id == station_id).all()


def get_available_bikes_count(db: Session, station_id: int) -> int:
    """Get count of available bikes in a station"""
    return db.query(Bike).filter(
        Bike.station_id == station_id,
        Bike.status == BikeStatus.AVAILABLE,
        Bike.is_active == True,
    ).count()


def get_total_bikes_count(db: Session, station_id: int) -> int:
    """Get total count of bikes in a station"""
    return db.query(Bike).filter(
        Bike.station_id == station_id,
        Bike.is_active == True,
    ).count()


def get_bike_by_id(db: Session, bike_id: int) -> Optional[Bike]:
    """Get bike by ID"""
    return db.query(Bike).filter(Bike.id == bike_id).first()


def get_bike_by_qr_code(db: Session, qr_code_hash: str) -> Optional[Bike]:
    """Get bike by QR code hash"""
    return db.query(Bike).filter(Bike.qr_code_hash == qr_code_hash).first()


def create_bike(
    db: Session,
    station_id: int,
    qr_code_hash: str,
    model: Optional[str] = None,
) -> Optional[Bike]:
    """Create a new bike"""
    # Verify station exists and has capacity
    station = get_station_by_id(db, station_id)
    if not station:
        return None
    
    current_count = get_total_bikes_count(db, station_id)
    if current_count >= station.capacity:
        return None
    
    # Check if QR code already exists
    existing_bike = get_bike_by_qr_code(db, qr_code_hash)
    if existing_bike:
        return None
    
    bike = Bike(
        station_id=station_id,
        qr_code_hash=qr_code_hash,
        model=model,
        status=BikeStatus.AVAILABLE,
    )
    db.add(bike)
    db.commit()
    db.refresh(bike)
    return bike


def update_bike_status(
    db: Session,
    bike_id: int,
    status: BikeStatus,
) -> Optional[Bike]:
    """Update bike status"""
    bike = get_bike_by_id(db, bike_id)
    if not bike:
        return None
    
    bike.status = status
    db.commit()
    db.refresh(bike)
    return bike


def mark_bike_maintenance(
    db: Session,
    bike_id: int,
) -> Optional[Bike]:
    """Mark bike as under maintenance"""
    from datetime import datetime, timezone
    bike = get_bike_by_id(db, bike_id)
    if not bike:
        return None
    
    bike.status = BikeStatus.MAINTENANCE
    bike.last_maintenance = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bike)
    return bike


def retire_bike(db: Session, bike_id: int) -> Optional[Bike]:
    """Retire a bike from service"""
    bike = get_bike_by_id(db, bike_id)
    if not bike:
        return None
    
    bike.status = BikeStatus.RETIRED
    bike.is_active = False
    db.commit()
    db.refresh(bike)
    return bike


def get_stations_by_availability(
    db: Session,
    limit: int = 10,
) -> List[tuple]:
    """Get stations sorted by available bikes (lowest first)"""
    result = db.query(
        Station.id,
        Station.name,
        func.count(Bike.id).label("total_bikes"),
        func.sum(
            func.cast(
                Bike.status == BikeStatus.AVAILABLE,
                type_=Integer
            )
        ).label("available_bikes"),
    ).outerjoin(Bike).group_by(Station.id).order_by("available_bikes").limit(limit).all()
    
    return result


def get_all_bikes(db: Session, skip: int = 0, limit: int = 100) -> List[Bike]:
    """Get all bikes with pagination"""
    return db.query(Bike).offset(skip).limit(limit).all()


from sqlalchemy import Integer
