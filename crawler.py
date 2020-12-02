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


def get_metadata(extension_links):
    metadata_list = []

    for link in extension_links:
        html = requests.get(link)

        page = BeautifulSoup(html.content, "html.parser")

        name = page.find("h1", class_="AddonTitle").text
        author = page.find("span", class_="AddonTitle-author").text

        metadata = {
            'name': name.replace(author, "").strip(),
            'author': author.replace("by ", "").strip(),
            'number_of_users': int(page.find("dd", class_="MetadataCard-content").text.replace(",", "")),
            'stars_average': float(page.find('div', class_="AddonMeta-rating-title").text.replace(" Stars", "")),
            'comment_link': cons.BASE_URL + page.find('a', class_='AddonMeta-reviews-title-link').get('href')
        }

        metadata_list.append(metadata)

    return metadata_list



# links = ["https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search", "https://addons.mozilla.org/en-US/firefox/addon/video-downloadhelper/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search"]
#
# print(get_metadata(links))
