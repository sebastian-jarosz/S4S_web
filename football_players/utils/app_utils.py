from datetime import datetime


def parse_transfermarkt_date(transfermarkt_date):
    return datetime.strptime(transfermarkt_date, "%b %d, %Y").strftime("%Y-%m-%d")
