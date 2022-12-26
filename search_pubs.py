'''
Searches publication titles on google scholar using scholarly.
'''


import os
import sys
import scholarly as scholar
import util
import config as cfg
import random
import time


N_WORKERS = 1
sleep_time = 60


def serialize_result(result):
    keys = [
        '_filled',
        'bib',
        'citedby',
        'id_scholarcitedby',
        'source',
        'url_scholarbib',
    ]
    return {k: getattr(result, k, None) for k in keys}


def search_pub(query):
    search = scholar.search_pubs_query(query)
    try:
        result = next(iter(search))
        result = serialize_result(result)
    except StopIteration:
        result = {}
    return result


def get_search_result_path(uid, query, base_dir):
    filename = '{}_{}.json'.format(util.slugify(query), str(uid)[:8])
    return os.path.join(base_dir, filename)


def search_pub_and_save(uid, query, base_dir):
    data = {
        'uid': uid,
        'query': query,
        'success': True,
        'message': '',
        'result': {},
    }
    path = get_search_result_path(uid, query, base_dir)
    if os.path.isfile(path):
        data = util.load_json(path)
        if data['success'] and data['result']:
            print('skipping query "{}" with results'.format(query))
            return
    print('executing query "{}"'.format(query))
    try:
        result = search_pub(query)
        data['result'] = result
    except Exception as e:
        error_msg = str(e)
        print('ERROR for query "{}": "{}"'.format(query, error_msg))
        data['success'] = False
        data['message'] = error_msg
    util.save_json(path, data)
    print('saved query "{}" to {}'.format(query, path))
    global sleep_time
    if not data['result']:
        sleep_time *= 1.1
    print('sleeping for {:.2f} seconds'.format(sleep_time))
    time.sleep(sleep_time)
    return data


def search_pubs(queries, dst_dir):
    random.shuffle(queries)
    args = [(uid, q, dst_dir) for uid, q in queries]
    results = util.parallelize(
        search_pub_and_save, args, n_threads=N_WORKERS, star=True)
    return results


def main():
    if len(sys.argv) >= 3:
        queries_list_path = sys.argv[1]
        results_dir_path = sys.argv[2]
        queries = util.read_lines(queries_list_path)
        queries = list(enumerate(queries))
    else:
        papers_metadata = util.load_json(cfg.paths['papers-metadata'])
        queries = [(m['uid'], m['title']) for m in papers_metadata]
        results_dir_path = cfg.paths['search-pubs-results-dir']


    util.mk_dir_if_needed(results_dir_path)
    search_pubs(queries, results_dir_path)

    print('saved results to', results_dir_path)


if __name__ == '__main__':
    main()
