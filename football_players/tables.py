import django_tables2 as tables
from django.db.models import F, Count
from django_tables2 import A

from .models import *


class CountryTable(tables.Table):
    description = tables.LinkColumn('country details', args=[A('id')], verbose_name="Country name")
    transfermarkt_hyperlink = tables.URLColumn(attrs={'a': {'target': '_blank'}})

    class Meta:
        model = Country
        template_name = "tables/responsive-table.html"


class LeagueTable(tables.Table):
    description = tables.LinkColumn('league details', args=[A('id')], verbose_name="League name")
    country = tables.LinkColumn('country details', args=[A('country.id')])
    transfermarkt_hyperlink = tables.URLColumn(attrs={'a': {'target': '_blank'}})

    class Meta:
        model = League
        template_name = "tables/responsive-table.html"


class SeasonTable(tables.Table):
    description = tables.LinkColumn('season details', args=[A('id')], verbose_name="Season name")
    league = tables.LinkColumn('league details', args=[A('league.id')])
    transfermarkt_hyperlink = tables.URLColumn(attrs={'a': {'target': '_blank'}})

    class Meta:
        model = Season
        template_name = "tables/responsive-table.html"


class QueueTable(tables.Table):
    number = tables.LinkColumn('queue details', args=[A('id')], text=lambda record: 'Queue {0}'.format(record.number),
                               verbose_name="Queue name")
    transfermarkt_hyperlink = tables.URLColumn(attrs={'a': {'target': '_blank'}})

    class Meta:
        model = Queue
        template_name = "tables/responsive-table.html"


class MatchTable(tables.Table):
    match = tables.LinkColumn('match details', args=[A('id')], order_by=("first_team", "second_team"),
                              text=lambda record: '{0} vs. {1}'.format(record.first_team, record.second_team))
    queue = tables.LinkColumn('queue details', args=[A('queue.id')])
    transfermarkt_hyperlink = tables.URLColumn(attrs={'a': {'target': '_blank'}})

    class Meta:
        model = Match
        # Change order of columns - match (explicitly created), rest of columns from DB
        sequence = ('match', '...')
        template_name = "tables/responsive-table.html"


class PlayerTable(tables.Table):
    player = tables.LinkColumn('player details', args=[A('id')],
                               text=lambda record: '{0} {1}'.format(record.first_name, record.last_name))
    transfermarkt_hyperlink = tables.URLColumn(attrs={'a': {'target': '_blank'}})

    class Meta:
        model = Player
        # Change order of columns - player (explicitly created), rest of columns from DB
        sequence = ('player', '...')
        template_name = "tables/responsive-table.html"


class MatchPlayerTable(tables.Table):
    player = tables.LinkColumn('player details', args=[A('player.id')],
                               text=lambda record: '{0} {1}'.format(record.player.first_name, record.player.last_name))
    position = tables.TemplateColumn('{{ record.player.position }}')

    time = tables.Column(verbose_name="Minutes in match")

    class Meta:
        model = MatchPlayer
        # Change order of columns - player (explicitly created), rest of columns from DB
        sequence = ('player', 'position', '...')
        template_name = "tables/responsive-table.html"


class GoalTable(tables.Table):
    match = tables.LinkColumn('match details', args=[A('match.id')])

    class Meta:
        model = Goal
        template_name = "tables/responsive-table.html"


class AssistTable(tables.Table):
    match = tables.LinkColumn('match details', args=[A('match.id')])

    class Meta:
        model = Assist
        template_name = "tables/responsive-table.html"


class BestPlayersTable(tables.Table):
    name = tables.LinkColumn('player details', args=[A('id')], order_by=("first_name", "last_name"),
                             text=lambda record: '{0} {1}'.format(record.first_name, record.last_name))
    goals = tables.TemplateColumn('{{ record.goal_set.count }}')
    assists = tables.TemplateColumn('{{ record.assist_set.count }}')
    time_in_matches = tables.TemplateColumn('{{ record.get_time_sum_from_all_matches }}')
    transfermarkt_hyperlink = tables.URLColumn(attrs={'a': {'target': '_blank'}})

    def order_time_in_matches(self, queryset, is_descending):
        queryset = queryset.annotate(
            time_in_matches=(Sum('matchplayer__time'))
        ).order_by(("-" if is_descending else "") + "time_in_matches")
        return queryset, True

    def order_goals(self, queryset, is_descending):
        queryset = queryset.annotate(
            goals=(Count('goal'))
        ).order_by(("-" if is_descending else "") + "goals")
        return queryset, True

    def order_assists(self, queryset, is_descending):
        queryset = queryset.annotate(
            assists=(Count('assist'))
        ).order_by(("-" if is_descending else "") + "assists")
        return queryset, True

    class Meta:
        model = Player
        # Change order of columns - name (explicitly created), rest of columns from DB
        sequence = ('name', '...')
        template_name = "tables/responsive-table.html"
