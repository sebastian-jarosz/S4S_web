import codecs
import requests
from bs4 import BeautifulSoup


def get_page_soup_from_file(html_path):
    f = codecs.open(html_path, 'r', encoding='utf-8', errors=' ignore')
    page_soup = BeautifulSoup(f, 'html.parser')
    return page_soup


def get_page_soup_from_hyperlink(hyperlink):
    # For pretending being a browser
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # Getting full page
    page_tree = requests.get(hyperlink, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')
    return page_soup


# Additional validation for empty queue pages
def get_queue_page_soup_from_hyperlink(hyperlink):
    page_soup = get_page_soup_from_hyperlink(hyperlink)
    score_tags = page_soup.findAll("span", {"class": "matchresult"})

    if len(score_tags) == 0:
        page_soup = None

    return page_soup
