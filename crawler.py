from bs4 import BeautifulSoup
import requests
import constant as cons


def get_extensions_urls(last_page):
    href_list = []

    for i in range(1, last_page + 1):
        page = requests.get("https://addons.mozilla.org/en-US/firefox/search/?page=" + str(i) + "&type=extension")

        href_all = BeautifulSoup(page.content, "html.parser").body.find_all("a", class_="SearchResult-link")

        for href in href_all:
            href_list.append(cons.BASE_URL + href.get('href'))

    return href_list
