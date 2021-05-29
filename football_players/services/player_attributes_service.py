import football_players.constants as const
from datetime import datetime
from .scraping_service import get_page_soup_from_hyperlink
from ..models import Player, Position, ManagementAgency, DominatingFoot


def update_attributes_for_all_players():
    for player in Player.objects.all():
        update_attributes_for_player(player)


def update_attributes_for_player(player):
    page_soup = get_page_soup_from_hyperlink(player.transfermarkt_hyperlink)

    date_of_birth = get_date_of_birth_from_page_soup(page_soup)
    position = get_position_from_page_soup(page_soup)
    management_agency = get_management_agency_from_page_soup(page_soup)
    dominating_foot = get_dominating_foot_from_page_soup(page_soup)

    player.date_of_birth = date_of_birth
    player.position = position
    player.agency = management_agency
    player.foot = dominating_foot

    try:
        player.save()
    except:
        print("Error for player ID:%i %s\t- NOT UPDATED" % (player.id, str(player)))

    print("Player ID:%i %s\t- UPDATED" % (player.id, str(player)))


def get_date_of_birth_from_page_soup(page_soup):
    # Get birthdate and trim left and right white signs
    try:
        date_of_birth = page_soup.find("span", {"itemprop": "birthDate"}).text.strip().split('(')[0].strip()
        date_of_birth = datetime.strptime(date_of_birth, "%b %d, %Y").strftime("%Y-%m-%d")
    except Exception:
        date_of_birth = const.NO_INFORMATION

    return date_of_birth


def get_position_from_page_soup(page_soup):
    # Get span with text "Position:" then get next span with actual position of player, then stip spaces
    position_description = page_soup.find("span", text="Position:").findNext("span").text.strip()

    position, created = Position.objects.get_or_create(
        defaults={
            'description': position_description
        },
        description__iexact=position_description
    )

    if created:
        print("Position %s\t- CREATED" % position.description)

    return position


def get_management_agency_from_page_soup(page_soup):
    # Get span with text "Agent:", get next span with actual player agency,
    # then strip spaces (try in case there is an agent)
    try:
        management_agency_description = page_soup.find("span", text="Agent:").findNext("span").text.strip()
        if management_agency_description.endswith("..."):
            management_agency_description = page_soup.find("span", text="Agent:").findNext("a")["title"]
            if management_agency_description.startswith("<span"):
                management_agency_description = management_agency_description.split("\"")[3]
    except Exception:
        management_agency_description = const.NO_INFORMATION

    management_agency, created = ManagementAgency.objects.get_or_create(
        defaults={
            'name': management_agency_description
        },
        name__iexact=management_agency_description
    )

    if created:
        print("Management Agency %s\t- CREATED" % management_agency.name)
    else:
        print("Management Agency %s\t- EXISTS" % management_agency.name)

    return management_agency


def get_dominating_foot_from_page_soup(page_soup):
    try:
        dominating_foot_description = page_soup.find("th", text="Foot:").findNext("td").getText()
        # To have only one way to show no dominating foot information
        if dominating_foot_description == "N/A":
            dominating_foot_description = const.NO_INFORMATION
    except:
        dominating_foot_description = const.NO_INFORMATION

    dominating_foot, created = DominatingFoot.objects.get_or_create(
        defaults={
            'description': dominating_foot_description
        },
        description__iexact=dominating_foot_description
    )

    if created:
        print("Dominating Foot %s\t- CREATED" % dominating_foot.description)

    return dominating_foot
