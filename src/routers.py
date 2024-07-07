from datetime import datetime

from fastapi import HTTPException, APIRouter, Query, Path
from starlette.responses import JSONResponse
from loguru import logger
from src.dao import get_latest_geometries, get_latest_geometry_by_vehicle_id, get_track_by_vehicle_id

routers = APIRouter()


@routers.get("/vehicles")
async def get_vehicles():
    try:
        latest_geometries = await get_latest_geometries()
        return JSONResponse(content=latest_geometries, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@routers.get("/vehicles/{vehicle_id}")
async def get_vehicle_by_id(
        vehicle_id: int = Path(description="Example - 10620")
):
    try:
        latest_geometry = await get_latest_geometry_by_vehicle_id(vehicle_id)
        if latest_geometry is None:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return JSONResponse(content=latest_geometry, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@routers.get("/vehicles/{vehicle_id}/track")
async def get_track_by_vehicle_id_endpoint(
        vehicle_id: int = Path(description="Example - 10620"),
        start_time: datetime = Query(description="Example - 2023-12-06 04:12:12-0800"),
        end_time: datetime = Query(description="Example - 2023-12-06 04:16:12-0800")
):
    try:
        track = await get_track_by_vehicle_id(vehicle_id, start_time, end_time)
        if not track:
            raise HTTPException(status_code=404, detail="No track found")
        return JSONResponse(content=track, media_type="application/geo+json")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
