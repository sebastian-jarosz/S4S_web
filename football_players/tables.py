import django_tables2 as tables
from .models import *


class PlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"

