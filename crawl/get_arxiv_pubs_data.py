#!/usr/bin/env python3

import user
import json
import os


WEBDRIVER_PATH = '/home/erik/Downloads/chromedriver'
QUERY_URL = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=attention&terms-0-field=title&terms-1-operator=OR&terms-1-term=attentional&terms-1-field=title&terms-2-operator=OR&terms-2-term=attentive&terms-2-field=title&terms-3-operator=OR&terms-3-term=attention&terms-3-field=abstract&terms-4-operator=OR&terms-4-term=attentional&terms-4-field=abstract&terms-5-operator=OR&terms-5-term=attentive&terms-5-field=abstract&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=2014&date-to_date=2019&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first'
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

    usr = user.ArxivUser(
        driver=user.get_chrome_driver(WEBDRIVER_PATH, page_load_timeout=60))
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
