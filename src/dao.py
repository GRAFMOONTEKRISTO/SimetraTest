from datetime import datetime

from sqlalchemy import select, and_

from sqlalchemy import func
from geojson import Feature, FeatureCollection, Point

from src.db import async_session_maker
from src.models import VehicleData


async def get_latest_geometries() -> list:
    """get_latest_geometries асинхронно получает последние геометрии для каждого транспортного средства из базы данных"""
    async with (async_session_maker() as session):
        # Создаем запрос stmt для получения максимального значения gps_time для каждого транспортного средства.
        # Запрос группирует данные по vehicle_id и выбирает максимальное значение gps_time для каждой группы.
        stmt = select(
            VehicleData.vehicle_id, func.max(VehicleData.gps_time)
            .label('max_gps_time')
        ).group_by(VehicleData.vehicle_id).subquery()

        # Создаем подзапрос latest_geometries_stmt для получения последних геометрий для каждого транспортного средства.
        # Выбираем все столбцы из таблицы VehicleData, где vehicle_id и gps_time соответствуют значениям из stmt
        latest_geometries_stmt = select(VehicleData).where(
            and_(VehicleData.vehicle_id == stmt.c.vehicle_id, VehicleData.gps_time == stmt.c.max_gps_time))

        latest_geometries = await session.execute(latest_geometries_stmt)
        latest_geometries = latest_geometries.scalars().all()

        vehicles_data = []
        for vehicle in latest_geometries:
            vehicle_dict = {}
            for column in vehicle.__table__.columns:
                value = getattr(vehicle, column.key)
                if isinstance(value, datetime):
                    value = value.isoformat()
                vehicle_dict[column.key] = value
            vehicles_data.append(vehicle_dict)
    return vehicles_data


async def get_latest_geometry_by_vehicle_id(vehicle_id: int) -> dict:
    async with async_session_maker() as session:
        # Выбирает последнюю запись из таблицы VehicleData для указанного vehicle_id,
        # сортируя по времени gps_time в порядке убывания
        stmt = select(VehicleData).where(VehicleData.vehicle_id == vehicle_id).order_by(
            VehicleData.gps_time.desc()).limit(1)
        latest_geometry = await session.execute(stmt)
        latest_geometry = latest_geometry.scalars().first()

        # Преобразуем объект latest_geometry в словарь response_content, форматируя datetime значения в ISO строку
        response_content = {}
        for column in latest_geometry.__table__.columns:
            value = getattr(latest_geometry, column.key)
            if isinstance(value, datetime):
                response_content[column.key] = value.isoformat()
            else:
                response_content[column.key] = value
    return response_content


async def get_track_by_vehicle_id(vehicle_id: int, start_time: datetime, end_time: datetime) -> FeatureCollection:
    async with async_session_maker() as session:
        # Выбираем записи из VehicleData для указанного vehicle_id в диапазоне времени от start_time до end_time,
        # сортируя по gps_time в порядке возрастания
        stmt = select(VehicleData).where(
            and_(
                VehicleData.vehicle_id == vehicle_id,
                VehicleData.gps_time >= start_time,
                VehicleData.gps_time <= end_time
            )
        ).order_by(VehicleData.gps_time.asc())
        result = await session.execute(stmt)
        track = result.scalars().all()

        # Преобразуем список точек трека в коллекцию географических объектов (FeatureCollection),
        # где каждая точка представлена как объект Feature с геометрией Point и свойством time
        def create_feature(point):
            return Feature(
                geometry=Point((point.longitude, point.latitude)),
                properties={"time": point.gps_time.isoformat()}
            )

        features = [create_feature(point) for point in track]
        track_feature_collection = FeatureCollection(features)

        response_content = track_feature_collection

    return response_content
