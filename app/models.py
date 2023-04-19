# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2023-04-17 07:05:15
# @Last Modified by:   Noaghzil
# @Last Modified time: 2023-04-19 08:14:33
from tortoise.models import Model
from tortoise import fields

class Tournament(Model):
    """
      比赛
    """
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    events: fields.ReverseRelation["Event"]

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return self.name

    class Meta:
        # If you don't specify table name, it will be generated from model name
        # by converting CamelCase to snake_case
        table = "tournament"
        table_description = "比赛"


class Event(Model):
    """
     赛事
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="赛事名称")
    # References to other models are defined in format
    # "{app_name}.{model_name}" - where {app_name} is defined in tortoise config
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events', description="所属比赛")
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team', description="参赛队伍")

    def __str__(self):
        return self.name
    
    class Meta:
        table = "event"
        table_description = "赛事"


class Team(Model):
    """
      队伍
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    events: fields.ManyToManyRelation[Event]

    def __str__(self):
        return self.name
    
    class Meta:
        table = "team"
        table_description = "队伍"
