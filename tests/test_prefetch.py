from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.query_utils import Prefetch


import logging
logging.basicConfig()
logger = logging.getLogger('tortoise')
logger.setLevel(logging.DEBUG)

class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    events: fields.ReverseRelation["Event"]

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    tournament: fields.ForeignKeyRelation[Tournament] = fields.ForeignKeyField(
        "models.Tournament", related_name="events"
    )
    participants: fields.ManyToManyRelation["Team"] = fields.ManyToManyField(
        "models.Team", related_name="events", through="event_team"
    )

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    events: fields.ManyToManyRelation[Event]

    def __str__(self):
        return self.name


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    tournament = await Tournament.create(name="tournament")
    tournament_2 = await Tournament.create(name="tournament2")
    await Event.create(name="First", tournament=tournament)
    await Event.create(name="Second", tournament=tournament)
    await Event.create(name="Third", tournament=tournament_2)

    logger.info(f"Filtered events ======================")
    
    tournament_with_filtered = (
        await Tournament.all()
        .prefetch_related(Prefetch("events", queryset=Event.filter(name="First")))
    )
    logger.info(f"Filtered events: {tournament_with_filtered}")
    for tournament in tournament_with_filtered:
        logger.info(f"Filtered events name: {tournament.name}")
        for event in tournament.events:
            logger.info(f"Filtered events name: {event.name}")
        
    logger.info(f"Filtered  tournament.event ======================")
    tournament_with_filtered = (
        await Tournament.all().filter(events__name="First").prefetch_related("events")
    )
    logger.info(f"Filtered tournament.event: {tournament_with_filtered}")
    for tournament in tournament_with_filtered:
        logger.info(f"Filtered tournament.event: {tournament.name}")
        for event in tournament.events:
            logger.info(f"Filtered tournament.event: {event.name}")

    logger.info(f"All events ======================") 
    tournament_all_events = await Tournament.all().prefetch_related("events")
    logger.info(f"All events: {tournament_all_events}")
    for tournament in tournament_all_events:
        logger.info(f"All events name: {tournament.name}")
        for event in tournament.events:
            logger.info(f"All events name: {event.name}")
        
    logger.info(f"Filtered to_attr ======================")
    tournament_with_filtered_to_attr = (
        await Tournament.all()
        .prefetch_related(
            Prefetch("events", queryset=Event.filter(name="First"), to_attr="to_attr_events_first"),
            Prefetch(
                "events", queryset=Event.filter(name="Second"), to_attr="to_attr_events_second"
            ),
        )
        .first()
    )
    for event in tournament_with_filtered_to_attr.to_attr_events_first:
        logger.info(f"Filtered name: {event.name}")
    for event in tournament_with_filtered_to_attr.to_attr_events_second:
        logger.info(f"Filtered name: {event.name}")


if __name__ == "__main__":
    run_async(run())
