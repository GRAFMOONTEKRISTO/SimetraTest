import asyncio
import datetime

import pandas as pd
from sqlalchemy import insert

from src.db import async_session_maker
from src.models import VehicleData


def parse_excel_file(excel_file):
    """
    Парсит Excel файл и возвращает список данных

    :param excel_file: путь к Excel файлу
    :return: список данных из Excel файла
    """
    xl = pd.ExcelFile(excel_file)
    tables = xl.sheet_names
    data = []

    for table in tables:
        table_data = xl.parse(table)
        # использую сложночитаемый list comprehension, потому что он ускорит процесс парсинга на 30-50%
        data.extend(
            [[datetime.datetime.fromisoformat(str(x)) if isinstance(x, str) and x.startswith('202') else x for x in row]
             for row in table_data.values.tolist()])
    return data


async def add_data_pars_to_db(data):
    async with (async_session_maker() as session):
        for row in data:
            add_vehicle_data = (
                insert(VehicleData)
                .values(
                    id=row[0],
                    longitude=row[1],
                    latitude=row[2],
                    speed=row[3],
                    gps_time=row[4],
                    vehicle_id=row[5]
                )
            )
            await session.execute(add_vehicle_data)
        await session.commit()


data = parse_excel_file('test_data.xlsx')
asyncio.run(add_data_pars_to_db(data))
