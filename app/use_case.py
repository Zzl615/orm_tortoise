# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2023-04-17 08:07:29
# @Last Modified by:   Noaghzil
# @Last Modified time: 2023-04-17 08:10:43
from app.models import Tournament, Event, Team
from tortoise.query_utils import Prefetch

async def usecase_one():
    tournament = await Tournament.create(name="tournament")
    await Event.create(name="First", tournament=tournament)
    await Event.create(name="Second", tournament=tournament)
    tournament_with_filtered = (
        await Tournament.all()
        .prefetch_related(Prefetch("events", queryset=Event.filter(name="First")))
        .first()
    )
    print(tournament_with_filtered)
    print(await Tournament.first().prefetch_related("events"))