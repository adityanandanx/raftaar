from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base
import enum


class BikeStatus(str, enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    bikes = relationship("Bike", back_populates="station")

    def __repr__(self):
        return f"<Station(id={self.id}, name={self.name}, lat={self.latitude}, lng={self.longitude})>"


class Bike(Base):
    __tablename__ = "bikes"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False, index=True)
    qr_code_hash = Column(String, unique=True, nullable=False, index=True)
    model = Column(String, nullable=True)
    status = Column(Enum(BikeStatus), default=BikeStatus.AVAILABLE, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    last_maintenance = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    station = relationship("Station", back_populates="bikes")

    def __repr__(self):
        return f"<Bike(id={self.id}, station_id={self.station_id}, qr_code={self.qr_code_hash}, status={self.status})>"
