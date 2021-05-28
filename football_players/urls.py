from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('country', views.country, name="country"),
    path('league', views.league, name="league"),
    path('season', views.season, name="season"),
    path('queue', views.queue, name="queue"),
    path('team', views.team, name="team"),
    path('player', views.player, name="player")
]
