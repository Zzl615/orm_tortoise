# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2023-04-17 08:07:29
# @Last Modified by:   Noaghzil
# @Last Modified time: 2023-04-19 08:11:56
from app.models import Tournament, Event, Team
from tortoise.query_utils import Prefetch


async def case_one():
    print("===============case_one==================")
    tournament_with_filtered = (
        await Tournament.all()
        .prefetch_related(Prefetch("events", queryset=Event.filter(name="First")))
        .first() # .first() 集合all()中的第一个元素
    )
    print("tournament_with_filtered: {}".format(tournament_with_filtered.name))
    for event in tournament_with_filtered.events:
        print("tournament_with_filtered.event: {}".format(event))

async def case_two():
    print("===============case_two==================")
    tournaments = await Tournament.all().prefetch_related("events")
    for tournament in tournaments:
        print("tournaments: {}".format(tournament.name))
        for event in tournament.events:
            print("tournaments.event: {}".format(event))

async def case_three():
    print("===============case_three==================")
    tournaments_with_filtered_to_attr = (
        await Tournament.all()
        .prefetch_related(
            Prefetch("events", queryset=Event.filter(name="First"), to_attr="first_events"),
            Prefetch(
                "events", queryset=Event.filter(name="Second"), to_attr="second_events"
            ),
        )
    )
    for tournament in tournaments_with_filtered_to_attr:
        print("tournaments_with_filtered_to_attr: {}".format(tournament.name))
        for event in tournament.first_events:
            print("tournaments_with_filtered_to_attr.first_events: {}".format(event))
        for event in tournament.second_events:
            print("tournaments_with_filtered_to_attr.second_events: {}".format(event))


async def prefetch_usecase():
    tournament = await Tournament.create(name="tournament")
    await Tournament.create(name="tournament1")
    await Tournament.create(name="tournament2")
    await Event.create(name="First", tournament=tournament)
    await Event.create(name="Second", tournament=tournament)
    await case_one()
    await case_two()
    await case_three()
    
    
    
   