from django.http import HttpResponse
from football_players.country_service import get_countries_from_file
from football_players.league_service import get_leagues_from_all_countries
from football_players.season_service import create_seasons_for_all_leagues
from football_players.queue_service import create_queues_for_all_seasons
from football_players.team_service import create_teams_for_all_seasons


def index(request):
    return HttpResponse("Hello, this is our football app")


def country(request):
    get_countries_from_file()
    return HttpResponse("get_countries_from_file invoked")


def league(request):
    get_leagues_from_all_countries()
    return HttpResponse("get_leagues_from_all_countries invoked")


def season(request):
    create_seasons_for_all_leagues()
    return HttpResponse("create_seasons_for_all_leagues invoked")


def queue(request):
    create_queues_for_all_seasons()
    return HttpResponse("create_queues_for_all_seasons invoked")


def team(request):
    create_teams_for_all_seasons()
    return HttpResponse("create_teams_for_all_seasons invoked")



