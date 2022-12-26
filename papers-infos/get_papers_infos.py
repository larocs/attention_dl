import user
import json
import os
import time
import random
import math
from multiprocessing.pool import ThreadPool


WEBDRIVER_PATH = './chromedriver'
SRC_PATH = '/home/erik/proj/litrev/crawl/pubs/pubs_uniq_titles.csv'
DST_DIR_PATH = './results_paper_info'
MAX_N_RETRIES = 3
N_WORKERS = 4
MIN_SLEEP_TIME = 1
MAX_SLEEP_TIME = 3


def get_paper_info(usr, query):
    data = {
        'query': query,
        'success': True,
        'message': '',
        'result': {},
    }
    try:
        result = usr.get_paper_info(query)
        data['result'] = result
    except Exception as e:
        print('ERROR on query "{}": "{}"'.format(query, e))
        data['success'] = False
        data['message'] = str(e)
    return data


def save_json(path, dct):
    with open(path, 'w') as f:
        json.dump(dct, f, indent=4, sort_keys=True)


def get_paper_info_path(i, query):
    for c in ' _.{}()%$#@!*&+=[]/|':
        query = query.replace(c, '-')
    filename = '{}_{}.json'.format(i, query)
    path = os.path.join(DST_DIR_PATH, filename)
    return path


def save_paper_info(path, data):
    save_json(path, data)
    return path


def consume(usr, i, query):
    print('in query {}: "{}"'.format(i+1, query))

    path = get_paper_info_path(i, query)
    if os.path.exists(path):
        print('{} exists, skipping'.format(path))
        return

    for j in range(MAX_N_RETRIES):
        data = get_paper_info(usr, query)
        if data['success']:
            break
        else:
            print('trying again')
            continue

    save_paper_info(path, data)
    print('saved query to', path)

    sleep_time = random.uniform(MIN_SLEEP_TIME, MAX_SLEEP_TIME)
    print('sleeping for {} seconds'.format(sleep_time))
    time.sleep(sleep_time)


def consume_group(group):
    usr = user.User(WEBDRIVER_PATH)
    for i, query in group:
        try:
            consume(usr, i, query)
        except Exception as e:
            print('ERROR2 in {}, {}: {}'.format(i, query, e))
            continue


def main():
    if not os.path.isdir(DST_DIR_PATH):
        os.makedirs(DST_DIR_PATH)

    with open(SRC_PATH) as f:
        queries = [l.strip() for l in f if l.strip()]
    print('loaded {} queries'.format(len(queries)))

    args = list(enumerate(queries))
    args = [(i, q) for i, q in args
        if not os.path.isfile(get_paper_info_path(i, q))]
    print('filtered to {} args'.format(len(args)))

    chunk_size = math.ceil(len(args)/N_WORKERS)
    groups = [args[i:i+chunk_size] for i in range(0, len(args), chunk_size)]
    print('got', len(groups), 'groups')

    pool = ThreadPool(N_WORKERS)
    pool.map(consume_group, groups)


if __name__ == '__main__':
    main()
