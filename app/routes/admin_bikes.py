"""Admin routes for bike and station management"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.user import User, UserRole
from app.models.bike import Bike, BikeStatus
from app.routes.auth import get_current_user
from app.schemas.bike import (
    StationCreate, StationResponse, StationWithBikeCount,
    BikeCreate, BikeResponse, BikeWithStation, StationUpdate
)
from app.services.bike_service import (
    create_station, get_all_stations, get_station_by_id,
    create_bike, get_all_bikes, get_bike_by_id,
    update_bike_status, mark_bike_maintenance, retire_bike,
    get_bikes_by_station, get_available_bikes_count, get_total_bikes_count,
    get_stations_by_availability, update_station,
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure user is admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


# ==================== Station Endpoints ====================

@router.post("/stations", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
def create_new_station(
    station: StationCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new bike station (admin only)"""
    new_station = create_station(
        db=db,
        name=station.name,
        latitude=station.latitude,
        longitude=station.longitude,
        capacity=station.capacity,
    )
    
    logger.info(f"Admin {admin_user.id} created station {new_station.id}: {station.name}")
    
    return StationResponse.from_orm(new_station)


@router.get("/stations", response_model=list[StationWithBikeCount])
def get_stations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all stations with bike counts (admin only)"""
    stations = get_all_stations(db, skip=skip, limit=limit)
    
    result = []
    for station in stations:
        available = get_available_bikes_count(db, station.id)
        total = get_total_bikes_count(db, station.id)
        
        result.append(StationWithBikeCount(
            id=station.id,
            name=station.name,
            latitude=station.latitude,
            longitude=station.longitude,
            capacity=station.capacity,
            created_at=station.created_at,
            updated_at=station.updated_at,
            available_bikes=available,
            total_bikes=total,
        ))
    
    return result


@router.get("/stations/{station_id}", response_model=StationWithBikeCount)
def get_station(
    station_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get single station with bike counts (admin only)"""
    station = get_station_by_id(db, station_id)
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station not found",
        )
    
    available = get_available_bikes_count(db, station.id)
    total = get_total_bikes_count(db, station.id)
    
    return StationWithBikeCount(
        id=station.id,
        name=station.name,
        latitude=station.latitude,
        longitude=station.longitude,
        capacity=station.capacity,
        created_at=station.created_at,
        updated_at=station.updated_at,
        available_bikes=available,
        total_bikes=total,
    )


@router.put("/stations/{station_id}", response_model=StationResponse)
def update_existing_station(
    station_id: int,
    station_update: StationUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update a station (admin only)"""
    station = update_station(
        db=db,
        station_id=station_id,
        name=station_update.name,
        capacity=station_update.capacity,
    )
    
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station not found",
        )
    
    logger.info(f"Admin {admin_user.id} updated station {station_id}")
    
    return StationResponse.from_orm(station)


# ==================== Bike Endpoints ====================

@router.post("/bikes", response_model=BikeResponse, status_code=status.HTTP_201_CREATED)
def add_bike_to_station(
    bike: BikeCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Add a bike to a station (admin only)"""
    new_bike = create_bike(
        db=db,
        station_id=bike.station_id,
        qr_code_hash=bike.qr_code_hash,
        model=bike.model,
    )
    
    if not new_bike:
        # Check if station exists or capacity issue
        station = get_station_by_id(db, bike.station_id)
        if not station:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Station not found",
            )
        
        # Check if QR code already exists
        from app.models.bike import Bike as BikeModel
        existing = db.query(BikeModel).filter(
            BikeModel.qr_code_hash == bike.qr_code_hash
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="QR code already exists",
            )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add bike to station (capacity exceeded or invalid data)",
        )
    
    logger.info(f"Admin {admin_user.id} added bike {new_bike.id} to station {bike.station_id}")
    
    return BikeResponse.from_orm(new_bike)


@router.get("/bikes", response_model=list[BikeWithStation])
def get_bikes_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: str = Query(None),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get all bikes with status filter (admin only)"""
    bikes = get_all_bikes(db, skip=skip, limit=limit)
    
    if status_filter:
        bikes = [b for b in bikes if b.status.value == status_filter]
    
    result = []
    for bike in bikes:
        result.append(BikeWithStation(
            id=bike.id,
            station_id=bike.station_id,
            qr_code_hash=bike.qr_code_hash,
            model=bike.model,
            status=bike.status.value,
            is_active=bike.is_active,
            last_maintenance=bike.last_maintenance,
            created_at=bike.created_at,
            updated_at=bike.updated_at,
            station_name=bike.station.name,
            station_lat=bike.station.latitude,
            station_lng=bike.station.longitude,
        ))
    
    return result


@router.get("/bikes/{bike_id}", response_model=BikeWithStation)
def get_bike_detail(
    bike_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get single bike detail (admin only)"""
    bike = get_bike_by_id(db, bike_id)
    if not bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found",
        )
    
    return BikeWithStation(
        id=bike.id,
        station_id=bike.station_id,
        qr_code_hash=bike.qr_code_hash,
        model=bike.model,
        status=bike.status.value,
        is_active=bike.is_active,
        last_maintenance=bike.last_maintenance,
        created_at=bike.created_at,
        updated_at=bike.updated_at,
        station_name=bike.station.name,
        station_lat=bike.station.latitude,
        station_lng=bike.station.longitude,
    )


@router.put("/bikes/{bike_id}/maintenance", response_model=BikeResponse)
def set_bike_maintenance(
    bike_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Mark bike as under maintenance (admin only)"""
    bike = mark_bike_maintenance(db, bike_id)
    
    if not bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found",
        )
    
    logger.info(f"Admin {admin_user.id} marked bike {bike_id} for maintenance")
    
    return BikeResponse.from_orm(bike)


@router.put("/bikes/{bike_id}/retire", response_model=BikeResponse)
def retire_existing_bike(
    bike_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Retire a bike (admin only)"""
    bike = retire_bike(db, bike_id)
    
    if not bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found",
        )
    
    logger.info(f"Admin {admin_user.id} retired bike {bike_id}")
    
    return BikeResponse.from_orm(bike)


@router.get("/stations/low-availability", response_model=list[dict])
def get_low_availability_stations(
    limit: int = Query(10, ge=1, le=50),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get stations with lowest availability (admin only)"""
    result = []
    stations = get_stations_by_availability(db, limit=limit)
    
    for station_id, name, total_bikes, available_bikes in stations:
        result.append({
            "station_id": station_id,
            "name": name,
            "total_bikes": total_bikes or 0,
            "available_bikes": available_bikes or 0,
        })
    
    return result
