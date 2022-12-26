import json
import os
import glob
import pandas as pd
from multiprocessing.pool import ThreadPool


INFOS_DIR_PATH = './results_paper_info'
DST_PATH = './papers_infos.csv'
DST_JSON_PATH = './papers_infos.json'
N_WORKERS = 4


def get_row(path):
    with open(path) as f:
        data = json.load(f)
    row = {
        #'row_num': int(os.path.basename(path).split('_')[0]),
        'title': data['query'],
        'success': data['success'],
        'n_citations': data.get('result', {}).get('n_citations'),
        'query_match': data.get('result', {}).get('query_match'),
        'result_title': data.get('result', {}).get('result_title'),
    }
    return row


def main():
    paths = glob.glob(os.path.join(INFOS_DIR_PATH, '*.json'))

    pool = ThreadPool(N_WORKERS)
    rows = pool.map(get_row, paths)

    df = pd.DataFrame(rows,
        columns=[
            'title',
            #'row_num',
            'success',
            'n_citations',
            'query_match',
            'result_title'])

    df.to_csv(DST_PATH, index=False)
    print('saved to', DST_PATH, flush=True)

    with open(DST_JSON_PATH, 'w') as f:
        json.dump(rows, f)
    print('saved json to', DST_JSON_PATH)


if __name__ == '__main__':
    main()
