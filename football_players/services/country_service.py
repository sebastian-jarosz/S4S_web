import os
from sys import platform
from .scraping_service import get_page_soup_from_file
from ..models import Country


# Data taken from file because of change in transfermarkt html structure
# get_countries_from_transfermarkt should be handled separately
def get_countries_from_file():
    # print(sys.path)
    html_path = os.path.realpath(__file__)
    if platform == "darwin":
        html_path = html_path.rsplit('/', 2)[0] + "/resources/transfermarkt.html"
    if platform == "win32":
        html_path = html_path.rsplit('\\', 2)[0] + "\\resources\\transfermarkt.html"

    page_soup = get_page_soup_from_file(html_path)

    countries_list = page_soup.find("select", {"data-placeholder": "Country"}).find_all('option')

    # delete empty record
    del countries_list[0]

    for country in countries_list:
        temp_country = {
            'description': country.text,
            'transfermarkt_id': int(country['value']),
            'transfermarkt_hyperlink': 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/'
                                       + country['value']
        }

        create_country(temp_country)


def create_country(temp_country):
    obj, created = Country.objects.get_or_create(
        transfermarkt_id=temp_country['transfermarkt_id'],
        transfermarkt_hyperlink=temp_country['transfermarkt_hyperlink'],
        defaults={
            'description': temp_country['description']
        }
    )

    if created:
        print("Country %s\t- Transfermarkt ID: %i\t- CREATED" % (obj.description, obj.transfermarkt_id))
    else:
        print("Country %s\t- Transfermarkt ID: %i\t- EXISTS" % (obj.description, obj.transfermarkt_id))
