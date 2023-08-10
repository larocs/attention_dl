#!/usr/bin/env python3

import user
import json
import os


WEBDRIVER_PATH = "C:\\Users\\DXT6\\Downloads\\bin\\chromedriver.exe"
# QUERY_URL = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=attention&terms-0-field=title&terms-1-operator=OR&terms-1-term=attentional&terms-1-field=title&terms-2-operator=OR&terms-2-term=attentive&terms-2-field=title&terms-3-operator=OR&terms-3-term=attention&terms-3-field=abstract&terms-4-operator=OR&terms-4-term=attentional&terms-4-field=abstract&terms-5-operator=OR&terms-5-term=attentive&terms-5-field=abstract&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=2014&date-to_date=2019&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first'
QUERY_URL = 'https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=dynamic+neural+network&terms-0-field=abstract&terms-3-operator=OR&terms-3-term=conditional+neural+network&terms-3-field=abstract&terms-5-operator=OR&terms-5-term=neural+architecture+search&terms-5-field=abstract&terms-7-operator=OR&terms-7-term=adaptive+neural+network&terms-7-field=abstract&terms-9-operator=OR&terms-9-term=gated+neural+network&terms-9-field=abstract&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first'
###
# QUERY_URL = 'https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=%22dynamic+neural+network%22&terms-0-field=title&terms-1-operator=OR&terms-1-term=%22dynamic+neural+network%22&terms-1-field=abstract&terms-8-operator=NOT&terms-8-term=%22dynamical+systems%22&terms-8-field=title&terms-9-operator=OR&terms-9-term=%22adaptive+neural+network%22&terms-9-field=title&terms-10-operator=OR&terms-10-term=%22adaptive+neural+network%22&terms-10-field=abstract&terms-11-operator=NOT&terms-11-term=%22dynamical+systems%22&terms-11-field=abstract&terms-12-operator=OR&terms-12-term=%22conditional+computation%22+%22neural+network%22&terms-12-field=title&terms-13-operator=OR&terms-13-term=%22conditional+computation%22+%22neural+network%22&terms-13-field=abstract&terms-14-operator=OR&terms-14-term=%22gated+neural+network%22&terms-14-field=title&terms-15-operator=OR&terms-15-term=%22gated+neural+network%22&terms-15-field=abstract&terms-16-operator=OR&terms-16-term=%22adaptive+inference%22+%22neural+network%22&terms-16-field=title&terms-17-operator=OR&terms-17-term=%22adaptive+inference%22+%22neural+network%22&terms-17-field=abstract&terms-18-operator=OR&terms-18-term=%22routing+neural+network%22&terms-18-field=title&terms-19-operator=OR&terms-19-term=%22routing+neural+network%22&terms-19-field=abstract&terms-20-operator=OR&terms-20-term=%22mixture+of+experts%22+%22neural+network%22&terms-20-field=title&terms-21-operator=OR&terms-21-term=%22mixture+of+experts%22+%22neural+network%22&terms-21-field=abstract&terms-22-operator=OR&terms-22-term=%22merging+of+experts%22+%22neural+network%22&terms-22-field=title&terms-23-operator=OR&terms-23-term=%22merging+of+experts%22+%22neural+network%22&terms-23-field=abstract&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=100&order=-announced_date_first'
###
DST_DIR_PATH = './arxiv_papers_infos'


def get_publication_data(usr, page_num, result_num, result_elem):
    data = {
        'query_url': QUERY_URL,
        'result': {},
        'page_num': page_num,
        'result_num': result_num,
    }
    try:
        result = usr.get_publication_data(result_elem)
        data['result'] = result
        if data['result']['submission_date'] is not None:
            data['result']['submission_date'] = \
                data['result']['submission_date'].isoformat()
    except Exception as e:
        print('ERROR: "{}"'.format(e))
        data['success'] = False
        data['message'] = str(e)
    return data


def save_json(path, dct):
    with open(path, 'w') as f:
        json.dump(dct, f, indent=4, sort_keys=True)


def get_publication_data_path(result):
    filename = '{}_{}_{}.json'.format(
        result['page_num'], result['result_num'],
        str(result['result'].get('arxiv_id', None)).replace('.', '-'))
    path = os.path.join(DST_DIR_PATH, filename)
    return path


def main():
    if not os.path.isdir(DST_DIR_PATH):
        os.makedirs(DST_DIR_PATH)

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    _service = Service(executable_path=WEBDRIVER_PATH)
    _options = webdriver.ChromeOptions()
    _driver = webdriver.Chrome(service=_service, options=_options)
    usr = user.ArxivUser(
        # driver=user.get_chrome_driver(WEBDRIVER_PATH, page_load_timeout=60)
        driver=_driver
    )
    usr.access(QUERY_URL)

    page_num = 1
    while True:
        result_elems = usr.get_results_elems()
        for i, elem in enumerate(result_elems):
            result_num = i + 1
            print('on page #{}, result #{}'.format(page_num, result_num))
            result = get_publication_data(usr, page_num, result_num, elem)
            path = get_publication_data_path(result)
            save_json(path, result)
            print('saved result to', path)

        if not usr.go_to_next_results_page():
            break
        page_num += 1


if __name__ == '__main__':
    main()
