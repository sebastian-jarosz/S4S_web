import football_players.constants as const
import datetime as dt
from ..models import Season, ApplicationParameters, League
from ..utils.app_utils import *


def create_seasons_for_all_leagues():
    all_leagues = League.objects.all()
    pool = get_pool()
    pool.map(create_seasons_for_league, all_leagues)
    pool.close()


# Multithreading used
def create_seasons_for_not_excluded_leagues():
    not_excluded_leagues = League.objects.filter(is_excluded=False)
    pool = get_pool()
    pool.map(create_seasons_for_league, not_excluded_leagues)
    pool.close()


def create_seasons_for_league(league):
    start_year_param = ApplicationParameters.objects.get(name=const.START_YEAR)
    tmp_year = int(start_year_param.value)
    current_year = dt.datetime.now().year

    existing_seasons = Season.objects.filter(league=league.id, begin_year__gte=tmp_year, begin_year__lte=current_year)

    # TODO change (current_year-tmp_year+1) to be more clear + different range situation
    # (current_year-tmp_year+1) - get inclusive year diff
    if existing_seasons.count() == (current_year-tmp_year+1):
        print("%s seasons from %i to %i exist" % (league.description, tmp_year, current_year))
        return

    while tmp_year <= current_year:
        season_hyperlink = league.transfermarkt_hyperlink + "/plus/?saison_id=" + str(tmp_year)
        season_description = league.description + " " + str(tmp_year) + "/" + str(tmp_year + 1)
        begin_year = tmp_year
        create_season(league, season_hyperlink, season_description, begin_year)
        tmp_year += 1


def create_season(league, season_hyperlink, season_description, begin_year):
    obj, created = Season.objects.get_or_create(
        begin_year=begin_year,
        end_year=begin_year + 1,
        transfermarkt_hyperlink=season_hyperlink,
        defaults={
            'description': season_description,
            'league': league
        }
    )

    if created:
        print("Season %s\t- CREATED" % obj.description)
    else:
        print("Season %s\t- EXISTS" % obj.description)
