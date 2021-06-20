from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('service/country', views.country, name="country service"),
    path('service/league', views.league, name="league service"),
    path('service/season', views.season, name="season service"),
    path('service/queue', views.queue, name="queue service"),
    path('service/team', views.team, name="team service"),
    path('service/player', views.player, name="player service"),
    path('service/player/attributes', views.player_attributes, name="player attributes service"),
    path('service/match', views.match, name="match service"),
    path('service/match/events', views.match_events, name="match events service")
]
