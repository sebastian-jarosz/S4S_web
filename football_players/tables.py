import django_tables2 as tables
from django_tables2 import A

from .models import *


class CountryTable(tables.Table):
    description = tables.LinkColumn('country details', args=[A('id')])

    class Meta:
        model = Country
        template_name = "django_tables2/bootstrap.html"


class LeagueTable(tables.Table):
    description = tables.LinkColumn('league details', args=[A('id')])

    class Meta:
        model = League
        template_name = "django_tables2/bootstrap.html"


class SeasonTable(tables.Table):
    description = tables.LinkColumn('season details', args=[A('id')])

    class Meta:
        model = Season
        template_name = "django_tables2/bootstrap.html"


class QueueTable(tables.Table):
    number = tables.LinkColumn('queue details', args=[A('id')], text=lambda record: 'Queue {0}'.format(record.number))

    class Meta:
        model = Queue
        template_name = "django_tables2/bootstrap.html"


class PlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"


class GoalTable(tables.Table):
    match = tables.LinkColumn('match details', args=[A('match.id')])

    class Meta:
        model = Goal
        template_name = "django_tables2/bootstrap.html"


class AssistTable(tables.Table):
    match = tables.LinkColumn('match details', args=[A('match.id')])

    class Meta:
        model = Assist
        template_name = "django_tables2/bootstrap.html"
