import football_players.constants as const
from .scraping_service import get_page_soup_from_hyperlink
from ..models import Match, Goal, Player, Assist, MatchPlayer
from ..utils.app_utils import *
from time import sleep
import requests


# Multithreading used
def create_events_for_all_matches():
    all_matches = Match.objects.all()
    for match in all_matches:
        create_events_for_match(match)


# Multithreading used
def create_events_for_not_fetched_matches():
    attempts = 0
    not_fetched_matches = Match.objects.filter(are_event_fetched=False)

    # Needed in case of connection refuse (too many requests)
    while attempts < 100 and len(not_fetched_matches) > 0:
        for match in not_fetched_matches:
            try:
                create_events_for_match(match)
            except requests.exceptions.ConnectionError:
                attempts += 1
                sleep(10)


def create_events_for_match(match):
    page_soup = get_page_soup_from_hyperlink(match.transfermarkt_hyperlink)
    season = match.get_season()

    starting_line_up_player_ids = get_starting_line_up_player_ids_from_page_soup(page_soup)
    in_player_ids, out_player_ids = get_substitutions_in_and_out_player_ids_from_page_soup(page_soup)
    goal_player_ids, assist_player_ids = get_goal_and_assist_player_ids_from_page_soup(page_soup)

    participating_players_dicts = []

    # IDs for all players involved in match
    for player_id in starting_line_up_player_ids + in_player_ids:
        player_dict = {'player_id': player_id, 'match_id': match.get_transfermarkt_id_as_string()}
        participating_players_dicts.append(player_dict)

    participating_players_dicts = get_hyperlinks_for_participating_players(participating_players_dicts, season)

    multiprocessing.set_start_method("fork", force=True)
    pool = get_pool()
    participating_players_dicts = pool.map(get_minutes_for_player, participating_players_dicts)
    pool.close()
    pool.join()

    # Save all goals to DB
    create_all_goals(goal_player_ids, match)
    # Save all assists to DB
    create_all_assists(assist_player_ids, match)

    # Save all Player - Match relations to DB
    for player_dict in participating_players_dicts:
        player_id = player_dict['player_id']

        player = get_player_by_transfermarkt_id(player_id)

        create_match_player_relation(player, match, player_dict['minutes'])

    match.are_event_fetched = True
    match.save()
    print("All events for match ID:%i date:%s between %s and %s\t- CREATED" %
          (match.id, str(match.date), match.first_team.name, match.second_team.name))


def get_starting_line_up_player_ids_from_page_soup(page_soup):
    starting_line_up_ids_tags = page_soup.findAll("span", {
        "class": ["aufstellung-rueckennummer-name", "spielprofil_tooltip", "tooltipstered"]})

    # Starting line up in case of different html structure
    if len(starting_line_up_ids_tags) == 0:
        line_ups_tag = page_soup.find("h2", text="Line-Ups")
        starting_line_up_tags = line_ups_tag.parent.parent if line_ups_tag is not None else None
        if starting_line_up_tags is not None:
            starting_line_up_ids_tags = starting_line_up_tags.findAll("a",
                                                                      {"class": ["spielprofil_tooltip", "tooltipstered"]})

    transfermarkt_players_ids = []

    if starting_line_up_ids_tags is not None:
        for id_tag in starting_line_up_ids_tags:
            transfermarkt_players_ids.append(id_tag['id'])

    return transfermarkt_players_ids


def get_goal_and_assist_player_ids_from_page_soup(page_soup):
    sb_tore_tag = page_soup.find("div", {"id": "sb-tore"})
    goal_table_record_tags = sb_tore_tag.findAll("div", {"class": "sb-aktion-aktion"}) \
        if sb_tore_tag is not None else None

    goal_player_ids = []
    assist_player_ids = []

    if goal_table_record_tags is not None:
        for goal_table_record_tag in goal_table_record_tags:
            player_tags = goal_table_record_tag.findAll("a", {"class": "wichtig"})
            for i in range(0, len(player_tags)):
                # if even number - Goal
                if i % 2 == 0:
                    goal_player_ids.append((player_tags[i])['id'])
                # if odd number - Assist
                else:
                    assist_player_ids.append((player_tags[i])['id'])

    return goal_player_ids, assist_player_ids


def get_hyperlinks_for_participating_players(participating_players_dicts, season):
    for player_dict in participating_players_dicts:
        player_hyperlink = const.TRANSFERMARKT_MAIN_PAGE_URL + "/a/leistungsdatendetails/spieler/" \
                           + player_dict['player_id'] + "/plus/0?saison=" + str(season.begin_year)
        player_dict['hyperlink'] = player_hyperlink

    return participating_players_dicts


def get_substitutions_in_and_out_player_ids_from_page_soup(page_soup):
    substitutions_table_tags = page_soup.find("div", {"id": "sb-wechsel"})

    in_player_ids = []
    out_player_ids = []

    if substitutions_table_tags is not None:
        out_player_span_tags = substitutions_table_tags.findAll("span", {"class": "sb-aktion-wechsel-aus"})
        in_player_span_tags = substitutions_table_tags.findAll("span", {"class": "sb-aktion-wechsel-ein"})

        in_player_tags = []
        out_player_tags = []

        for in_player_span_tag in in_player_span_tags:
            in_player_tags.extend(in_player_span_tag.findAll("a", {"class": "wichtig"}))

        for out_player_span_tag in out_player_span_tags:
            out_player_tags.extend(out_player_span_tag.findAll("a", {"class": "wichtig"}))

        for i in range(0, len(in_player_tags)):
            in_player_ids.append((in_player_tags[i])['id'])

        for i in range(0, len(out_player_tags)):
            out_player_ids.append((out_player_tags[i])['id'])

    return in_player_ids, out_player_ids


def get_minutes_for_player(player_dict):
    hyperlink = player_dict['hyperlink']
    match_id = player_dict['match_id']

    page_soup = get_page_soup_from_hyperlink(hyperlink)

    match_tag = page_soup.find("a", {"id": match_id})
    match_tag_parent = match_tag.findParent() if match_tag is not None else None
    match_tag_next_parent = match_tag_parent.findParent() if match_tag_parent is not None else None
    minutes_tag = match_tag_next_parent.find("td", {"class": "rechts"}) if match_tag_next_parent is not None else None
    minutes = minutes_tag.getText() if minutes_tag is not None else 0

    player_dict['minutes'] = int(minutes.split('\'')[0]) if (minutes and minutes != 0) else 0

    return player_dict


def get_player_by_transfermarkt_id(transfermarkt_id):
    try:
        player = Player.objects.get(transfermarkt_id=int(transfermarkt_id))
    except Player.DoesNotExist:
        player = None

    return player


def create_all_goals(goal_player_ids, match):
    for player_id in goal_player_ids:
        player = get_player_by_transfermarkt_id(player_id)
        create_goal(player, match)


def create_goal(player, match):
    if player is None or match is None:
        return

    obj = Goal.objects.create(
        player=player,
        match=match
    )

    print("Goal by %s\t in match %s\t - CREATED" % (player, match.date))


def create_all_assists(assist_player_ids, match):
    for player_id in assist_player_ids:
        player = get_player_by_transfermarkt_id(player_id)
        create_assist(player, match)


def create_assist(player, match):
    if player is None or match is None:
        return

    obj = Assist.objects.create(
        player=player,
        match=match
    )

    print("Assist by %s\t in match %s\t - CREATED" % (player, match.date))


def create_match_player_relation(player, match, time):
    if player is None or match is None:
        return

    obj, created = MatchPlayer.objects.get_or_create(
        player=player,
        match=match,
        time=time
    )

    if created:
        print("Relation - player %s\t in match %s\t - CREATED" % (player, match.date))
    else:
        print("Relation - player %s\t in match %s\t - EXISTS" % (player, match.date))
