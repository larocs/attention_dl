import user


WEBDRIVER_PATH = "/usr/bin/chromedriver"
# QUERY_URL = 'https://dblp.uni-trier.de/search?q=attention%7Cattentive%7Cattentional%20year%3A2019%7C2018%7C2017%7C2016%7C2015%7C2014%20type%3AJournal_Articles%3A%7Ctype%3AConference_and_Workshop_Papers%3A'
QUERY_URL = "https://dblp.uni-trier.de/search?q=social%20network%20content%20year%3A2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C2014%20type%3AJournal_Articles%3A%7Ctype%3AConference_and_Workshop_Papers%3A"
DST_PATH = "dblp_bibtex_links.csv"


def save_lines(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            print(line, file=f)


def main():
    usr = user.DblpUser(
        driver=user.get_chrome_driver(WEBDRIVER_PATH, page_load_timeout=60))
    usr.access(QUERY_URL)

    print('getting pub elems...', flush=True)
    elems = usr.get_all_pub_elems()
    print('done getting pub elems')

    links = []
    for i, elem in enumerate(elems):
        try:
            link = usr.get_bibtex_link(elem)
        except Exception as e:
            print('ERROR on elem #{}: {}'.format(i + 1, e))
            continue
        links.append(link)
    print('got {} links'.format(len(links)))

    save_lines(DST_PATH, links)
    print('saved to', DST_PATH)


if __name__ == '__main__':
    main()
