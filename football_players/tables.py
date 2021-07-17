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
    country = tables.LinkColumn('country details', args=[A('country.id')])

    class Meta:
        model = League
        template_name = "django_tables2/bootstrap.html"


class SeasonTable(tables.Table):
    description = tables.LinkColumn('season details', args=[A('id')])
    league = tables.LinkColumn('league details', args=[A('league.id')])

    class Meta:
        model = Season
        template_name = "django_tables2/bootstrap.html"


class QueueTable(tables.Table):
    number = tables.LinkColumn('queue details', args=[A('id')], text=lambda record: 'Queue {0}'.format(record.number))

    class Meta:
        model = Queue
        template_name = "django_tables2/bootstrap.html"


class MatchTable(tables.Table):
    match = tables.LinkColumn('match details', args=[A('id')],
                              text=lambda record: '{0} vs. {1}'.format(record.first_team, record.second_team))
    queue = tables.LinkColumn('queue details', args=[A('queue.id')])

    class Meta:
        model = Match
        # Change order of columns - match (explicitly created), rest of columns from DB
        sequence = ('match', '...')
        template_name = "django_tables2/bootstrap.html"


class PlayerTable(tables.Table):
    player = tables.LinkColumn('player details', args=[A('id')],
                               text=lambda record: '{0} {1}'.format(record.first_name, record.last_name))

    class Meta:
        model = Player
        # Change order of columns - match (explicitly created), rest of columns from DB
        sequence = ('player', '...')
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
