#!/usr/bin/env python3

import json
import os
import pandas as pd
import glob
from multiprocessing.pool import ThreadPool


SRC_DIR_PATH = './arxiv_papers_infos'
DST_PATH = './arxiv_papers.csv'
N_WORKERS = 8


def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def get_row(path):
    data = load_json(path)
    row = data['result']
    if 'authors' in row:
        row['authors'] = ' AND '.join(row['authors'])
    if 'abstract' in row:
        del row['abstract']
    return row


def main():
    paths = glob.glob(os.path.join(SRC_DIR_PATH, '*.json'))

    pool = ThreadPool(N_WORKERS)
    rows = pool.map(get_row, paths)

    df = pd.DataFrame(
        rows, columns=['arxiv_id', 'title', 'authors', 'submission_date'])
    df.to_csv(DST_PATH, index=False)

    print('saved to', DST_PATH)


if __name__ == '__main__':
    main()
