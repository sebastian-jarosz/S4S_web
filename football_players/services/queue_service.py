import datetime as dt
import football_players.constants as const
from .scraping_service import get_queue_page_soup_from_hyperlink
from ..models import Season, ApplicationParameters, Queue
from ..utils.app_utils import *


# Multithreading used
def create_queues_for_all_seasons():
    all_seasons = Season.objects.all()
    pool = get_pool()
    pool.map(create_queues_for_season, all_seasons)


def create_queues_for_season(season):
    max_queue_number_param = ApplicationParameters.objects.get(name=const.MAX_QUEUE_NUMBER)

    # Range +1 because of needed values from 1 to MAX_QUEUE_NUMBER inclusive
    for queue_number in range(1, int(max_queue_number_param.value) + 1):
        # Check if queue exists
        queue = Queue.objects.filter(number=queue_number, season=season.id)
        if queue:
            print("Queue %i from %s already exists" % (queue_number, season.description))
            continue

        queue_hyperlink = season.transfermarkt_hyperlink + "&spieltag=" + str(queue_number)

        # If page_soup is empty - no more valid queues will be retrieved
        page_soup = get_queue_page_soup_from_hyperlink(queue_hyperlink)
        if not page_soup:
            break

        create_queue(queue_number, queue_hyperlink, season)


def create_queue(queue_number, queue_hyperlink, season):
    obj, created = Queue.objects.get_or_create(
        number=queue_number,
        transfermarkt_hyperlink=queue_hyperlink,
        defaults={
            'season': season
        }
    )

    if created:
        print("Queue %i\t- Season %s\t- CREATED" % (obj.number, season.description))
    else:
        print("Queue %i\t- Season %s\t- EXISTS" % (obj.number, season.description))
