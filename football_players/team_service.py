import football_players.constants as const
from .scraping_service import get_page_soup_from_hyperlink
from .models import Season, Team


def create_teams_for_all_seasons():
    # TODO
    for season in Season.objects.filter(description__contains='ekstraklasa '):
        create_teams_for_season(season)


def create_teams_for_season(season):
    page_soup = get_page_soup_from_hyperlink(season.transfermarkt_hyperlink)
    divs = page_soup.find_all(name='div', class_='box')
    for div in divs:
        # Only teams table div contains 'To complete table' footer
        complete_table_tag = div.find(title='To complete table')
        if complete_table_tag is not None:
            # td tags contain teams hyperlinks
            for td in div.find_all(name='td', class_='no-border-links hauptlink'):
                a_tag = td.find(name='a')

                # href without saison_id to have more generic hyperlink for team
                team_hyperlink = const.TRANSFERMARKT_MAIN_PAGE_URL + a_tag['href'].split('/saison_id/')[0]
                team_transfermarkt_id = a_tag['id']
                team_name = a_tag.text

                create_team(team_name, team_hyperlink, team_transfermarkt_id)


def create_team(team_name, team_hyperlink, team_transfermarkt_id):
    obj, created = Team.objects.get_or_create(
        transfermarkt_id=team_transfermarkt_id,
        defaults={
            'name': team_name,
            'transfermarkt_hyperlink': team_hyperlink
        }
    )

    if created:
        print("Team %s\t- %s\t- CREATED" % (obj.transfermarkt_id, obj.name))
    else:
        print("Team %s\t- %s\t- EXISTS" % (obj.transfermarkt_id, obj.name))