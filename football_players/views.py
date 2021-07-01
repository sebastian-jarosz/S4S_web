from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .services.country_service import get_countries_from_file
from .services.league_service import *
from .services.season_service import *
from .services.queue_service import *
from .services.team_service import *
from .services.player_service import *
from .services.player_attributes_service import *
from .services.match_service import *
from .services.match_event_service import *


def index(request):
    return HttpResponse("Hello, this is our football app")


def country_service(request):
    get_countries_from_file()
    return HttpResponse("get_countries_from_file invoked")


def league_service(request):
    # get_leagues_from_all_countries()
    get_leagues_from_not_excluded_countries()
    return HttpResponse("get_leagues_from_all_countries invoked")


def season_service(request):
    # create_seasons_for_all_leagues()
    create_seasons_for_not_excluded_leagues()
    return HttpResponse("create_seasons_for_all_leagues invoked")


def queue_service(request):
    create_queues_for_all_seasons()
    return HttpResponse("create_queues_for_all_seasons invoked")


def team_service(request):
    # create_teams_for_all_seasons()
    create_teams_for_not_fetched_seasons()
    return HttpResponse("create_teams_for_not_fetched_seasons invoked")


def player_service(request):
    create_players_for_all_teams_and_not_fetched_seasons()
    return HttpResponse("create_players_for_all_teams_and_not_fetched_seasons invoked")


def player_attributes_service(request):
    update_attributes_for_not_updated_players()
    return HttpResponse("update_attributes_for_not_updated_players invoked")


def match_service(request):
    create_matches_for_not_fetched_queues()
    return HttpResponse("create_matches_for_not_fetched_queues invoked")


def match_events_service(request):
    create_events_for_not_fetched_matches()
    return HttpResponse("create_events_for_all_matches invoked")


def country(request):
    # Only not excluded countries are listed
    all_countries = Country.objects.filter(is_excluded=False)
    template = loader.get_template('players/country.html')
    context = {
        'all_countries': all_countries,
    }
    return HttpResponse(template.render(context, request))


def country_details(request, country_id):
    country_obj = get_object_or_404(Country, pk=country_id)
    return render(request, 'players/country_details.html', {'country': country_obj})


def league(request):
    # Only not excluded leagues are listed
    all_leagues = League.objects.filter(is_excluded=False)
    template = loader.get_template('players/league.html')
    context = {
        'all_leagues': all_leagues,
    }
    return HttpResponse(template.render(context, request))


def league_details(request, league_id):
    league_obj = get_object_or_404(League, pk=league_id)
    return render(request, 'players/league_details.html', {'league': league_obj})


def season_details(request, season_id):
    season_obj = get_object_or_404(Season, pk=season_id)
    return render(request, 'players/season_details.html', {'season': season_obj})


def queue_details(request, queue_id):
    queue_obj = get_object_or_404(Queue, pk=queue_id)
    return render(request, 'players/queue_details.html', {'queue': queue_obj})


def match_details(request, match_id):
    match_obj = get_object_or_404(Match, pk=match_id)
    all_players_from_match = MatchPlayer.objects.filter(match=match_obj).values('player')

    first_team_players = []
    second_team_players = []

    first_team_players_relations = PlayerTeam.objects.filter(team=match_obj.first_team, season=match_obj.queue.season)\
        .filter(player__in=all_players_from_match)
    second_team_players_relations = PlayerTeam.objects.filter(team=match_obj.second_team, season=match_obj.queue.season)\
        .filter(player__in=all_players_from_match)

    for player_team in first_team_players_relations:
        first_team_players.append(player_team.player)

    for player_team in second_team_players_relations:
        second_team_players.append(player_team.player)

    first_team_goals = match_obj.goal_set.filter(player__in=first_team_players)
    second_team_goals = match_obj.goal_set.filter(player__in=second_team_players)

    first_team_assists = match_obj.assist_set.filter(player__in=first_team_players)
    second_team_assists = match_obj.assist_set.filter(player__in=second_team_players)

    return render(request, 'players/match_details.html',
                  {
                      'match': match_obj,
                      'first_team_players': first_team_players,
                      'second_team_players': second_team_players,
                      'first_team_goals': first_team_goals,
                      'second_team_goals': second_team_goals,
                      'first_team_assists': first_team_assists,
                      'second_team_assists': second_team_assists
                  })


def player(request):
    all_players = Player.objects.all()
    template = loader.get_template('players/player.html')
    context = {
        'all_players': all_players,
    }
    return HttpResponse(template.render(context, request))


def player_details(request, player_id):
    player_obj = get_object_or_404(Player, pk=player_id)
    return render(request, 'players/player_details.html', {'player': player_obj})

