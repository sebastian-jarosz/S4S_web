from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django_tables2 import SingleTableView
from .services.country_service import *
from .services.league_service import *
from .services.season_service import *
from .services.queue_service import *
from .services.team_service import *
from .services.player_service import *
from .services.player_attributes_service import *
from .services.match_service import *
from .services.match_event_service import *
from .tables import *


def index(request):
    return render(request, 'index.html')


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
    country_table = CountryTable(all_countries,
                                 extra_columns=(('id', None), ('transfermarkt_id', None), ('is_excluded', None)))
    return render(request, 'players/country.html', {'country_table': country_table})


def country_details(request, country_id):
    country_obj = get_object_or_404(Country, pk=country_id)
    leagues_table = LeagueTable(country_obj.get_not_excluded_leagues(),
                                extra_columns=(('id', None), ('is_excluded', None),
                                               ('transfermarkt_id', None), ('country', None),))
    return render(request, 'players/country_details.html',
                  {
                      'country': country_obj,
                      'leagues_table': leagues_table
                  })


def league(request):
    # Only not excluded leagues are listed
    all_leagues = League.objects.filter(is_excluded=False)
    league_table = LeagueTable(all_leagues,
                               extra_columns=(('id', None), ('transfermarkt_id', None), ('is_excluded', None),))
    return render(request, 'players/league.html', {'league_table': league_table})


def league_details(request, league_id):
    league_obj = get_object_or_404(League, pk=league_id)
    seasons_table = SeasonTable(league_obj.get_all_seasons(), extra_columns=(('id', None), ('league', None), ))
    return render(request, 'players/league_details.html',
                  {
                      'league': league_obj,
                      'seasons_table': seasons_table
                  })


def season_details(request, season_id):
    season_obj = get_object_or_404(Season, pk=season_id)
    queues_table = QueueTable(season_obj.get_all_queues(), extra_columns=(('id', None), ('season', None), ))
    return render(request, 'players/season_details.html',
                  {
                      'season': season_obj,
                      'queues_table': queues_table
                  })


def queue_details(request, queue_id):
    queue_obj = get_object_or_404(Queue, pk=queue_id)
    matches_table = MatchTable(queue_obj.get_all_matches(),
                               extra_columns=(('id', None), ('first_team', None), ('second_team', None),
                                              ('queue', None)))
    return render(request, 'players/queue_details.html',
                  {
                      'queue': queue_obj,
                      'matches_table': matches_table
                  })


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

    # Players Tables
    first_team_players_table = PlayerTable(first_team_players, extra_columns=(('id', None), ('transfermarkt_id', None),
                                                                              ('first_name', None), ('last_name', None)))
    second_team_players_table = PlayerTable(second_team_players, extra_columns=(('id', None), ('transfermarkt_id', None),
                                                                                ('first_name', None), ('last_name', None)))
    # Goals Tables
    first_team_goals_table = GoalTable(first_team_goals,
                                       extra_columns=(('id', None), ('match', None))) if first_team_goals else None
    second_team_goals_table = GoalTable(second_team_goals,
                                        extra_columns=(('id', None), ('match', None))) if second_team_goals else None
    # Assist Tables
    first_team_assists_table = AssistTable(first_team_assists,
                                           extra_columns=(('id', None), ('match', None))) if first_team_assists else None
    second_team_assists_table = AssistTable(second_team_assists,
                                            extra_columns=(('id', None), ('match', None))) if second_team_assists else None

    return render(request, 'players/match_details.html',
                  {
                      'match': match_obj,
                      'first_team_players_table': first_team_players_table,
                      'second_team_players_table': second_team_players_table,
                      'first_team_goals_table': first_team_goals_table,
                      'second_team_goals_table': second_team_goals_table,
                      'first_team_assists_table': first_team_assists_table,
                      'second_team_assists_table': second_team_assists_table
                  })


class AllPlayersView(SingleTableView):
    model = Player
    table_class = PlayerTable
    template_name = 'players/player.html'


def player_details(request, player_id):
    player_obj = get_object_or_404(Player, pk=player_id)

    # extra_columns attr used to remove
    goal_table = GoalTable(player_obj.get_all_goals(), extra_columns=(('id', None), ('player', None),))
    assist_table = AssistTable(player_obj.get_all_assists(), extra_columns=(('id', None), ('player', None),))
    return render(request, 'players/player_details.html',
                  {
                      'player': player_obj,
                      'goal_table': goal_table,
                      'assist_table': assist_table
                  })


def best_players(request):
    all_players = Player.objects.all()
    # all_players = Player.objects.filter(id=1)
    return render(request, 'players/best_player.html', {'all_players': all_players})


class BestPlayersView(SingleTableView):
    model = Player
    table_class = PlayerTable
    template_name = 'players/best_player.html'
