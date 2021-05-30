import football_players.constants as const
import multiprocessing
from .scraping_service import get_page_soup_from_hyperlink
from ..models import Match, Team, Goal, Player, Assist, MatchPlayer
from ..utils.app_utils import parse_transfermarkt_date


def create_events_for_all_matches():
    # # TODO
    # for match in Match.objects.all():
    #     create_teams_for_season(queue)
    match = Match.objects.get(id=2)
    create_events_for_match(match)


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
    p = multiprocessing.Pool(50)
    participating_players_dicts = p.map(get_minutes_for_player, participating_players_dicts)
    p.close()

    # Save all goals to DB
    create_all_goals(goal_player_ids, match)
    # Save all assists to DB
    create_all_assists(assist_player_ids, match)

    # Save all Player - Match relations to DB
    for player_dict in participating_players_dicts:
        player_id = player_dict['player_id']
        player = Player.objects.get(transfermarkt_id=int(player_id))
        create_match_player_relation(player, match, player_dict['minutes'])


def get_starting_line_up_player_ids_from_page_soup(page_soup):
    starting_line_up_ids_tags = page_soup.findAll("span", {
        "class": ["aufstellung-rueckennummer-name", "spielprofil_tooltip", "tooltipstered"]})

    # Starting line up in case of different html structure
    if len(starting_line_up_ids_tags) == 0:
        starting_line_up_tags = page_soup.find("h2", text="Line-Ups").parent.parent
        starting_line_up_ids_tags = starting_line_up_tags.findAll("a",
                                                                  {"class": ["spielprofil_tooltip", "tooltipstered"]})

    transfermarkt_players_ids = []
    for id_tag in starting_line_up_ids_tags:
        transfermarkt_players_ids.append(id_tag['id'])

    return transfermarkt_players_ids


def get_goal_and_assist_player_ids_from_page_soup(page_soup):
    goal_table_record_tags = page_soup.find("div", {"id": "sb-tore"}).findAll("div", {"class": "sb-aktion-aktion"})

    goal_player_ids = []
    assist_player_ids = []

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

    out_player_span_tags = substitutions_table_tags.findAll("span", {"class": "sb-aktion-wechsel-aus"})
    in_player_span_tags = substitutions_table_tags.findAll("span", {"class": "sb-aktion-wechsel-ein"})

    in_player_tags = []
    out_player_tags = []
    in_player_ids = []
    out_player_ids = []

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

    minutes = page_soup.find("a", {"id": match_id}).findParent().findParent().find("td", {"class": "rechts"}).getText()

    player_dict['minutes'] = int(minutes.split('\'')[0])

    return player_dict


def create_all_goals(goal_player_ids, match):
    for player_id in goal_player_ids:
        player = Player.objects.get(transfermarkt_id=int(player_id))
        create_goal(player, match)


def create_goal(player, match):
    obj, created = Goal.objects.get_or_create(
        player=player,
        match=match
    )

    if created:
        print("Goal by %s\t in match %s\t - CREATED" % (player, match.date))
    else:
        print("Goal by %s\t in match %s\t - EXISTS" % (player, match.date))


def create_all_assists(assist_player_ids, match):
    for player_id in assist_player_ids:
        player = Player.objects.get(transfermarkt_id=int(player_id))
        create_assist(player, match)


def create_assist(player, match):
    obj, created = Assist.objects.get_or_create(
        player=player,
        match=match
    )

    if created:
        print("Assist by %s\t in match %s\t - CREATED" % (player, match.date))
    else:
        print("Assist by %s\t in match %s\t - EXISTS" % (player, match.date))


def create_match_player_relation(player, match, time):
    obj, created = MatchPlayer.objects.get_or_create(
        player=player,
        match=match,
        time=time
    )

    if created:
        print("Relation - player %s\t in match %s\t - CREATED" % (player, match.date))
    else:
        print("Relation - player %s\t in match %s\t - EXISTS" % (player, match.date))
