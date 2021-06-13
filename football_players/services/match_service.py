import football_players.constants as const
from .scraping_service import get_page_soup_from_hyperlink
from ..models import Match, Queue, Team
from ..utils.app_utils import *


# Multithreading used
def create_matches_for_all_queues():
    all_queues = Queue.objects.all()
    pool = get_pool()
    pool.map(create_matches_for_queue, all_queues)
    pool.close()
    pool.join()


# Multithreading used
def create_matches_for_not_fetched_queues():
    not_fetched_queues = Queue.objects.filter(are_matches_fetched=False)
    pool = get_pool()
    pool.map(create_matches_for_queue, not_fetched_queues)
    pool.close()
    pool.join()


def create_matches_for_queue(queue):
    page_soup = get_page_soup_from_hyperlink(queue.transfermarkt_hyperlink)
    score_tags = page_soup.findAll("span", {"class": "matchresult finished"})

    for score_tag in score_tags:
        team_related_tags = score_tag.parent.parent.parent.parent.findAll("td",
                                                                          {"class": "spieltagsansicht-vereinsname"})
        first_team, second_team = get_teams_from_team_related_tags(team_related_tags)
        match_transfermarkt_hyperlink = const.TRANSFERMARKT_MAIN_PAGE_URL + score_tag.find_parent("a")['href']
        date_tag = score_tag.parent.parent.parent.parent.findNext("tr").find("a")
        match_date = parse_transfermarkt_date(date_tag.text.strip()) if date_tag is not None else None

        create_match(first_team, second_team, match_transfermarkt_hyperlink, match_date, queue)

    queue.are_matches_fetched = True
    queue.save()
    print("All matches for queue %i in season %s\t- CREATED" % (queue.number, queue.season.description))


def get_teams_from_team_related_tags(team_related_tags):
    team_ids = []
    first_team = None
    second_team = None

    for tag in team_related_tags:
        if "hide-for-small" in tag["class"]:
            a_tag = tag.find("a", {"class": "vereinprofil_tooltip"})
            team_ids.append(a_tag["id"])

    first_team = Team.objects.get(transfermarkt_id=int(team_ids[0]))
    second_team = Team.objects.get(transfermarkt_id=int(team_ids[1]))

    return first_team, second_team


def create_match(first_team, second_team, transfermarkt_hyperlink, match_date, queue):
    obj, created = Match.objects.get_or_create(
        transfermarkt_hyperlink=transfermarkt_hyperlink,
        defaults={
            'first_team': first_team,
            'second_team': second_team,
            'date': match_date,
            'queue': queue
        }
    )

    if created:
        print("Match %s\t- %s\t - Date: %s - CREATED" % (obj.first_team, obj.second_team, obj.date))
    else:
        print("Match %s\t- %s\t - Date: %s - EXISTS" % (obj.first_team, obj.second_team, obj.date))
