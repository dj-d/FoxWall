from bs4 import BeautifulSoup
import requests
import constant as cons
from datetime import datetime
import time
from time import sleep


def get_extensions_urls(last_page):
    href_list = []

    for i in range(1, last_page + 1):
        html = requests.get("https://addons.mozilla.org/en-US/firefox/search/?page=" + str(i) + "&type=extension")

        sleep(3)

        href_all = BeautifulSoup(html.content, "html.parser").body.find_all("a", class_="SearchResult-link")

        for href in href_all:
            href_list.append(cons.BASE_URL + href.get('href'))

    return href_list


def get_metadata(extension_links):
    metadata_list = []

    for link in extension_links:
        html = requests.get(link)

        sleep(3)

        page = BeautifulSoup(html.content, "html.parser")

        name = page.find("h1", class_="AddonTitle").text
        author = page.find("span", class_="AddonTitle-author").text

        comment_link = cons.BASE_URL + page.find('a', class_='AddonMeta-reviews-title-link').get('href')

        # TODO: Aggiungere numero totale delle valutazioni
        metadata = {
            'name': name.replace(author, "").strip(),
            'author': author.replace("by ", "").strip(),
            'number_of_users': int(page.find("dd", class_="MetadataCard-content").text.replace(",", "")),
            'stars_average': float(page.find('div', class_="AddonMeta-rating-title").text.replace(" Stars", "")),
            'comment_link': get_comment_metadata(comment_link)
        }

        metadata_list.append(metadata)

    return metadata_list


def get_comment_metadata(comment_link):
    comments_list = []

    # TODO: To decomment
    # html = requests.get(comment_link)

    # sleep(3)

    # page = BeautifulSoup(html.content, "html.parser")

    # num_pages = page.find("div", class_="Paginate-page-number").text
    # num_pages = num_pages.split(" ")
    # num_pages = int(num_pages[3])
    #
    # print(num_pages)
    num_pages = 2

    for num_page in range(1, num_pages + 1):
        html = requests.get(comment_link + "&page=" + str(num_page))

        print("link: " + comment_link + "&page=" + str(num_page))
        page = BeautifulSoup(html.content, "html.parser")

        contents = page.find_all("div", class_="UserReview")

        for content in contents:
            comment = content.findChild("div", class_="ShowMoreCard-contents").text

            try:
                author = content.findChild("span", class_="AddonReviewCard-authorByLine")


                publishing_time = author.findChild("a").get("title")
                publishing_time = datetime.strptime(publishing_time, cons.COMMENT_TIME_FORMAT)
                publishing_timestamp = time.mktime(publishing_time.timetuple())

                author = author.text.replace(", " + author.findChild("a").text, "").replace("by ", "")

                stars = content.find("div", class_="Rating Rating--small").get("title")
                stars = stars.split(" ")
                del stars[::2]
                del stars[1:]
                stars = int(stars[0])

                comment_metadata = {
                    "author": author,
                    # "publishing_time": publishing_time,
                    "publishing_timestamp": publishing_timestamp,
                    "stars": stars,
                    "comment": comment
                }

                comments_list.append(comment_metadata)
            except Exception as e:
                # TODO: Manage response message
                # TODO: Manage unusual comments form

                print("Error author")
                print(content)

    return comments_list


extension_list = get_extensions_urls(1)
# print(extension_list)
metadata_list = get_metadata(extension_list)
# print(metadata_list)

f = open("../metadata.json", "w")
f.write(str(metadata_list))
f.close()
