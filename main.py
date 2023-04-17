# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2023-04-17 07:07:25
# @Last Modified by:   Noaghzil
# @Last Modified time: 2023-04-17 08:11:46
import asyncio
from tortoise import Tortoise, run_async
from tortoise.connection import connections
from app.use_case import usecase_one


async def init_db():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    print("ddd")
    # Generate the schema
    await Tortoise.generate_schemas()


def main():
    run_async(init_db())

def ts_main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.run_until_complete(connections.close_all(discard=True))

if __name__ == '__main__':
    run_async(init_db())
    run_async(usecase_one())