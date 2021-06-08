from django.http import HttpResponse
from .services.country_service import get_countries_from_file
from .services.league_service import *
from .services.season_service import *
from .services.queue_service import *
from .services.team_service import *
from .services.player_service import *
from .services.player_attributes_service import update_attributes_for_all_players
from .services.match_service import create_matches_for_all_queues
from .services.match_event_service import create_events_for_all_matches


def index(request):
    return HttpResponse("Hello, this is our football app")


def country(request):
    get_countries_from_file()
    return HttpResponse("get_countries_from_file invoked")


def league(request):
    # get_leagues_from_all_countries()
    get_leagues_from_not_excluded_countries()
    return HttpResponse("get_leagues_from_all_countries invoked")


def season(request):
    # create_seasons_for_all_leagues()
    create_seasons_for_not_excluded_leagues()
    return HttpResponse("create_seasons_for_all_leagues invoked")


def queue(request):
    create_queues_for_all_seasons()
    return HttpResponse("create_queues_for_all_seasons invoked")


def team(request):
    # create_teams_for_all_seasons()
    create_teams_for_not_fetched_seasons()
    return HttpResponse("create_teams_for_not_fetched_seasons invoked")


def player(request):
    create_players_for_all_teams_and_seasons()
    return HttpResponse("create_players_for_all_teams_and_seasons invoked")


def player_attributes(request):
    update_attributes_for_all_players()
    return HttpResponse("update_attributes_for_all_players invoked")


def match(request):
    create_matches_for_all_queues()
    return HttpResponse("create_matches_for_all_queues invoked")


def match_events(request):
    create_events_for_all_matches()
    return HttpResponse("create_events_for_all_matches invoked")

