#!/usr/bin/env python3


import json
import pandas as pd
import glob
import os
from multiprocessing.pool import ThreadPool


SRC_DIR_PATH = './pubs/jsons'
DST_PATH = './pubs/pubs.csv'
N_WORKERS = 8
COLUMNS = [
    'title',
    'authors',
    'year',
    'source',
    'uid',
    'abstract',
]


def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def get_row(path):
    row = load_json(path)
    row['authors'] = ';'.join(row['authors'])
    for k, v in row.items():
        row[k] = str(v).replace(',', ';').replace('\n', ' ').strip()
    return row


def main():
    paths = glob.glob(os.path.join(SRC_DIR_PATH, '*.json'))
    pool = ThreadPool(N_WORKERS)

    rows = pool.map(get_row, paths)

    df = pd.DataFrame(rows, columns=COLUMNS)
    df.to_csv(DST_PATH, index=False)
    print('saved to', DST_PATH)


if __name__ == '__main__':
    main()
