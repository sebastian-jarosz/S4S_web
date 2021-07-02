import django_tables2 as tables
from .models import *


class PlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"


class GoalTable(tables.Table):
    class Meta:
        model = Goal
        template_name = "django_tables2/bootstrap.html"


class AssistTable(tables.Table):
    class Meta:
        model = Assist
        template_name = "django_tables2/bootstrap.html"
