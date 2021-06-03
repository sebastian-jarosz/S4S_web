import multiprocessing
from datetime import datetime


def parse_transfermarkt_date(transfermarkt_date):
    return (datetime.strptime(transfermarkt_date, "%b %d, %Y").strftime("%Y-%m-%d")) if transfermarkt_date \
                                                                                        is not None else None


def get_pool():
    multiprocessing.set_start_method("fork", force=True)
    return multiprocessing.Pool(30)
