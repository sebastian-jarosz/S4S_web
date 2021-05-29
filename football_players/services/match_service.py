import football_players.constants as const
from .scraping_service import get_page_soup_from_hyperlink
from ..models import Match, Queue, Team
from ..utils.app_utils import parse_transfermarkt_date


def create_matches_for_all_queues():
    # TODO
    # for queue in Queue.objects.filter(description__contains='ekstraklasa '):
    #     create_teams_for_season(queue)
    queue = Queue.objects.get(id=1)
    create_matches_for_queue(queue)


def create_matches_for_queue(queue):
    page_soup = get_page_soup_from_hyperlink(queue.transfermarkt_hyperlink)
    score_tags = page_soup.findAll("span", {"class": "matchresult finished"})

    for score_tag in score_tags:
        team_related_tags = score_tag.parent.parent.parent.parent.findAll("td",
                                                                          {"class": "spieltagsansicht-vereinsname"})

        first_team, second_team = get_teams_from_team_related_tags(team_related_tags)
        match_transfermarkt_hyperlink = const.TRANSFERMARKT_MAIN_PAGE_URL + score_tag.find_parent("a")['href']
        match_date = parse_transfermarkt_date(score_tag.parent.parent.parent.parent.findNext("tr").find("a").text.strip())

        create_match(first_team, second_team, match_transfermarkt_hyperlink, match_date)


def get_teams_from_team_related_tags(team_related_tags):
    team_ids = []
    for tag in team_related_tags:
        if "hide-for-small" in tag["class"]:
            team_ids.append(tag.find("a")["id"])

    first_team = Team.objects.get(transfermarkt_id=int(team_ids[0]))
    second_team = Team.objects.get(transfermarkt_id=int(team_ids[1]))

    return first_team, second_team


def create_match(first_team, second_team, transfermarkt_hyperlink, match_date):
    obj, created = Match.objects.get_or_create(
        transfermarkt_hyperlink=transfermarkt_hyperlink,
        first_team=first_team,
        second_team=second_team,
        date=match_date
    )

    if created:
        print("Match %s\t- %s\t - Date: %s - CREATED" % (obj.first_team, obj.second_team, obj.date))
    else:
        print("Match %s\t- %s\t - Date: %s - EXISTS" % (obj.first_team, obj.second_team, obj.date))
