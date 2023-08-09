#!/usr/bin/env python3


import json
import glob
import os
import multiprocessing as mp
import math
import random
import user


WEBDRIVER_PATH = "C:\\Users\\DXT6\\Downloads\\bin\\chromedriver.exe"
SRC_DIR_PATH = './pubs/jsons'
DST_DIR_PATH = './updated_pubs/jsons'
N_WORKERS = 6


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def get_path(src_path):
    filename = os.path.basename(src_path)
    path = os.path.join(DST_DIR_PATH, filename)
    return path


def update_pub(usr, path):
    dst_path = get_path(path)
    if os.path.isfile(dst_path):
        return

    data = load_json(path)
    print('in pub uid={}'.format(data['uid']))

    if data['abstract'] is not None:
        return

    if data['url'] is None:
        return
    usr.access(data['url'])

    abstract = usr.get_abstract()
    if abstract is None:
        return
    data['abstract'] = abstract

    save_json(dst_path, data)
    print('saved updated work to', dst_path)


def update_pubs(paths):
    usr = user.AbstractGetter(
        driver=user.get_chrome_driver(WEBDRIVER_PATH, headless=True))

    for i, path in enumerate(paths):
        try:
            update_pub(usr, path)
        except Exception as e:
            print('ERROR on path #{}/{}: {}'.format(i+1, len(paths), e))
            continue


def get_chunks(lst, n_chunks):
    chunk_size = math.ceil(len(lst)/n_chunks)
    chunks = [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]
    return chunks


def main():
    if not os.path.isdir(DST_DIR_PATH):
        os.makedirs(DST_DIR_PATH)

    paths = glob.glob(os.path.join(SRC_DIR_PATH, '*.json'))
    random.shuffle(paths)

    path_chunks = get_chunks(paths, N_WORKERS)
    pool = mp.Pool(N_WORKERS)
    pool.map(update_pubs, path_chunks)


if __name__ == '__main__':
    main()
