import football_players.constants as const
from .scraping_service import get_page_soup_from_hyperlink
from ..models import Player, PlayerTeam, Team, Season


def create_players_for_all_teams_and_seasons():
    # TODO
    # for season in Season.objects.filter(description__contains='ekstraklasa '):
    #     for team in Team.objects.all():
    #         create_players_for_team_and_season(team, season)
    season = Season.objects.get(id=5821)
    team = Team.objects.get(id=1)

    create_players_for_team_and_season(team, season)


def create_players_for_team_and_season(team, season):
    # Players list for specific team and season needs separate hyperlink
    players_list_hyperlink = get_players_hyperlink_from_team_hyperlink(team.transfermarkt_hyperlink, season)
    print(players_list_hyperlink)
    page_soup = get_page_soup_from_hyperlink(players_list_hyperlink)

    # Players table
    table_div = page_soup.find("div", {"id": "yw1"})

    full_name_tags = table_div.find_all("span", {"class": "hide-for-small"})

    player_tags = []

    for fullNameTag in full_name_tags:
        player_tags.extend(fullNameTag.find_all("a", {"class": "spielprofil_tooltip"}))

    for playerTag in player_tags:
        transfermarkt_id = (playerTag['href'].rsplit('/', 1))[-1]
        first_name, last_name = split_full_name(playerTag.text)
        transfermarkt_hyperlink = const.TRANSFERMARKT_MAIN_PAGE_URL + playerTag['href']

        player = create_player(first_name, last_name, transfermarkt_id, transfermarkt_hyperlink)
        create_player_team_season_relation(player, team, season)


def get_players_hyperlink_from_team_hyperlink(team_hyperlink, season):
    return team_hyperlink.replace("spielplan", "kader") + "/?saison_id=" + str(season.begin_year)


def split_full_name(full_name):
    full_name_arr = full_name.split(' ', maxsplit=1)
    last_name = None  # In case of no Last Name

    first_name = full_name_arr[0]
    if ' ' in full_name:
        last_name = full_name_arr[1]

    return first_name, last_name


def create_player(first_name, last_name, transfermarkt_id, transfermarkt_hyperlink):
    player, created = Player.objects.get_or_create(
        transfermarkt_id=transfermarkt_id,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'transfermarkt_hyperlink': transfermarkt_hyperlink
        }
    )

    if created:
        print("Player %s\t- %s\t- CREATED" % (player.transfermarkt_id, str(player)))
    else:
        print("Player %s\t- %s\t- EXISTS" % (player.transfermarkt_id, str(player)))

    return player


def create_player_team_season_relation(player, team, season):
    obj, created = PlayerTeam.objects.get_or_create(
        team=team,
        player=player,
        season=season
    )

    if created:
        print("Relation %s\t- %s\t- %s\t- CREATED" % (str(player), team.name, season.description))
    else:
        print("Relation %s\t- %s\t- %s\t- EXISTS" % (str(player), team.name, season.description))