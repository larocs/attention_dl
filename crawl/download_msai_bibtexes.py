#!/usr/bin/env python3

import user


WEBDRIVER_PATH = "C:\\Users\\DXT6\\Downloads\\bin\\chromedriver.exe"
QUERY_URLS = [
    #'https://www.microsoft.com/en-us/research/search/?q=attention&facet%5Btax%5D%5Bmsr-content-type%5D%5B%5D=3&facet%5Bdate%5D%5Brange%5D%5Bfrom%5D=2014-1-1&facet%5Bdate%5D%5Brange%5D%5Bto%5D=2019-12-31',
    #'https://www.microsoft.com/en-us/research/search/?q=attentional&facet%5Bdate%5D%5Brange%5D%5Bfrom%5D=2014-1-1&facet%5Bdate%5D%5Brange%5D%5Bto%5D=2019-12-31&facet%5Btax%5D%5Bmsr-content-type%5D%5B%5D=3',
    'https://www.microsoft.com/en-us/research/search/?q=attentive&facet%5Btax%5D%5Bmsr-content-type%5D%5B%5D=3&facet%5Bdate%5D%5Brange%5D%5Bfrom%5D=2014-1-1&facet%5Bdate%5D%5Brange%5D%5Bto%5D=2019-12-31',
]


def get_key(elem):
    return hash(elem.text)


def get_bibtexes(usr, query_url):
    usr.access(query_url)

    page_num = 1

    while True:
        print('in page #{}'.format(page_num))

        explored_keys = set()
        while True:
            elems = {get_key(e): e for e in usr.get_pub_elems()}
            to_explore_keys = set(elems.keys()) - explored_keys
            if not to_explore_keys:
                break
            key = next(iter(to_explore_keys))
            elem = elems[key]
            usr.access_pub_page(elem)
            usr.download_bibtex()
            usr.driver.back()
            explored_keys.add(key)

        if not usr.go_to_next_page():
            break
        page_num += 1


def main():
    usr = user.MsAiUser(
        driver=user.get_chrome_driver(WEBDRIVER_PATH, page_load_timeout=60))

    for query_url in QUERY_URLS:
        get_bibtexes(usr, query_url)


if __name__ == '__main__':
    main()
