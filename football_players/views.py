from django.http import HttpResponse
from .services.country_service import get_countries_from_file
from .services.league_service import get_leagues_from_all_countries
from .services.season_service import create_seasons_for_all_leagues
from .services.queue_service import create_queues_for_all_seasons
from .services.team_service import create_teams_for_all_seasons
from .services.player_service import create_players_for_all_teams_and_seasons
from .services.player_attributes_service import update_attributes_for_all_players


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


def player(request):
    create_players_for_all_teams_and_seasons()
    return HttpResponse("create_players_for_all_teams_and_seasons invoked")


def player_attributes(request):
    update_attributes_for_all_players()
    return HttpResponse("update_attributes_for_all_players invoked")

