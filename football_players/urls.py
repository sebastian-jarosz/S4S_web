from django.conf.urls.static import static
from django.urls import path

from s4s_web import settings
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('api/country/', views.country_api, name="country api"),
    path('service/country/', views.country_service, name="country service"),
    path('api/league/', views.league_api, name="league api"),
    path('service/league/', views.league_service, name="league service"),
    path('api/season/', views.season_api, name="season api"),
    path('service/season/', views.season_service, name="season service"),
    path('api/queue/', views.queue_api, name="queue api"),
    path('service/queue/', views.queue_service, name="queue service"),
    path('api/team/', views.team_api, name="team api"),
    path('service/team/', views.team_service, name="team service"),
    path('api/match/', views.match_api, name="match api"),
    path('api/match/events/', views.match_events_api, name="match events api"),
    path('service/match/', views.match_service, name="match services"),
    path('api/player/', views.player_api, name="player api"),
    path('api/player/attributes/', views.player_attributes_api, name="player attributes api"),
    path('service/player/', views.player_service, name="player services"),
    path('country/', views.country, name="all countries list"),
    path('country/<int:country_id>/', views.country_details, name="country details"),
    path('league/', views.league, name="all leagues list"),
    path('league/<int:league_id>/', views.league_details, name="league details"),
    path('season/<int:season_id>/', views.season_details, name="season details"),
    path('queue/<int:queue_id>/', views.queue_details, name="queue details"),
    path('match/<int:match_id>/', views.match_details, name="match details"),
    path('player/', views.player, name="all players list"),
    path('player/<int:player_id>/', views.player_details, name="player details"),
] + static(settings.STATIC_URL)
