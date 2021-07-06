import django_tables2 as tables
from django_tables2 import A

from .models import *


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
