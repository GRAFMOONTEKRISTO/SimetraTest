from datetime import datetime

from sqlalchemy import DateTime, Column, Integer, Float, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class VehicleData(Base):
    __tablename__ = "vehicle_data"
    id = Column(Integer, primary_key=True)
    longitude = Column(Float)  # долгота
    latitude = Column(Float)  # широта
    speed = Column(Float)
    gps_time = Column(TIMESTAMP(timezone=True))
    vehicle_id = Column(Integer)

# from sqlalchemy import Column, Integer, Float, DateTime, TIMESTAMP
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.dialects.postgresql import UUID
# from geoalchemy2 import Geometry

# class VehicleData(Base):
#     __tablename__ = "vehicle_data"
#     id = Column(Integer, primary_key=True)
#     location = Column(Geometry('POINT', 4326))  # хранить долготу и широту как точку геометрии
#     speed = Column(Float)
#     gps_time = Column(TIMESTAMP(timezone=True))
#     vehicle_id = Column(UUID(as_uuid=True))  # хранить vehicle_id как UUID

