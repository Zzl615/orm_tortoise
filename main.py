# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2023-04-17 07:07:25
# @Last Modified by:   Noaghzil
# @Last Modified time: 2023-04-19 08:35:50
import asyncio
from tortoise import Tortoise, run_async
from tortoise.connection import connections
from app.use_case.prefetch import prefetch_usecase


async def init_db():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['app.models']}
    )
    print('db init')
    # Generate the schema
    await Tortoise.generate_schemas()


async def main():
    await init_db()
    await prefetch_usecase()

# def main():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(init_db())
#     loop.run_until_complete(connections.close_all(discard=True))

if __name__ == '__main__':
    run_async(main())