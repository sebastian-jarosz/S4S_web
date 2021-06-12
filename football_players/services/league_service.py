from .scraping_service import get_page_soup_from_hyperlink
from ..models import Country, League
from ..utils.app_utils import *


def get_leagues_from_all_countries():
    all_countries = Country.objects.all()
    pool = get_pool()
    pool.map(get_leagues_from_country, all_countries)
    pool.close()


# Multithreading used
def get_leagues_from_not_excluded_countries():
    not_excluded_countries = Country.objects.filter(is_excluded=False)
    pool = get_pool()
    pool.map(get_leagues_from_country, not_excluded_countries)
    pool.close()


def get_leagues_from_country(country):
    leagues = League.objects.filter(country=country.id)
    if leagues:
        print("Leagues for %s already exist." % country.description)
        return

    country_hyperlink = country.transfermarkt_hyperlink
    page_soup = get_page_soup_from_hyperlink(country_hyperlink)

    # Get main div - if no Leagues h2 will be None
    h2 = page_soup.find('h2', text="Domestic leagues & cups")
    if h2 is None:
        print("No leagues for %s on Transfermarkt." % country.description)
    else:
        domestic_leagues_and_cups_div = h2.find_parent('div', {'class': "box"})
        a_tags = domestic_leagues_and_cups_div.findChildren('a')

        # tabs included in Domestic Leagues and Cups div
        not_used_tags = ["compact", "detailed"]
        hyperlink_beginning = "https://www.transfermarkt.com/jumplist/spieltag/wettbewerb/"

        for tag in a_tags:
            # strip() - empty string are false so here we will only get tags with proper text
            if tag.text.strip() and tag.text.lower() not in not_used_tags:
                transfermarkt_id = tag['href'].split('/')[-1]
                temp_league = {
                    'description': tag.text,
                    'transfermarkt_id': transfermarkt_id,
                    'transfermarkt_hyperlink': hyperlink_beginning + transfermarkt_id
                }
                create_league(temp_league, country)


def create_league(temp_league, country):
    obj, created = League.objects.get_or_create(
        transfermarkt_id=temp_league['transfermarkt_id'],
        transfermarkt_hyperlink=temp_league['transfermarkt_hyperlink'],
        defaults={
            'description': temp_league['description'],
            'country': country
        }
    )

    if created:
        print("League %s\t- Transfermarkt ID: %s\t- CREATED" % (obj.description, obj.transfermarkt_id))
    else:
        print("League %s\t- Transfermarkt ID: %s\t- EXISTS" % (obj.description, obj.transfermarkt_id))
