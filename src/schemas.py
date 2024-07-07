from pydantic import BaseModel


class VehicleSchemas(BaseModel):
    id: int
    longitude: float
    latitude: float
    speed: int
    gps_time: str
    vehicle_id: int
