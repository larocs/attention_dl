'''
Extracts references from pdf files.
'''


import os
import requests

import util
import config as cfg


#script config
N_THREADS = cfg.n_threads * 4
PARSING_API_URL = 'http://freecite.library.brown.edu/citations/create'


def normalize_fields(data):
    if data.get('authors') is None:
        data['authors'] = []
    authors = {util.normalize_author(a) for a in data['authors']}
    data['norm-authors'] = sorted(authors)
    if data.get('title') is None:
        data['title'] = ''
    data['norm-title'] = util.normalize_title(data['title'])
    return data


def parse_raw_ref(ref):
    resp = requests.post(
        PARSING_API_URL,
        headers={
            'Accept': 'application/json',
        },
        data={
            'citation': ref,
        },
    )
    try:
        data = resp.json()[0]
        data = normalize_fields(data)
    except:
        print('ERROR with ref "{}", return_code = {}'.format(
            ref, resp.status_code))
        data = {}
    return data


def _parse_raw_refs(refs):
    data = []
    for ref in refs:
        data_ = parse_raw_ref(ref)
        print('parsed "{}" to "{}"'.format(ref, data_))
        if data_:
            data.append(data_)
    return data


def parse_raw_refs():
    refs = util.load_json(cfg.paths['raw-papers-refs'])
    # data = util.parallelize(_parse_raw_refs, list(refs.values()), N_THREADS)
    # refs = {k: v for k, v in zip(refs.keys(), data)}
    refs = {k: v for k, v in refs.items()}
    util.save_json(cfg.paths['papers-refs'], refs)

    print('saved papers refs to "{}"'.format(cfg.paths['papers-refs']))


def main():
    parse_raw_refs()


if __name__ == '__main__':
    main()
