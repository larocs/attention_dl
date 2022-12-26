import urllib.request as req
from multiprocessing.pool import ThreadPool
import os


SRC_PATH = './dblp_bibtex_links.csv'
DST_DIR_PATH = 'dblp_bibtexes'
N_WORKERS = 8


def get_path(link):
    filename = '_'.join(link.split('/')[-3:])
    path = os.path.join(DST_DIR_PATH, filename)
    return path


def download(link):
    path = get_path(link)
    if os.path.isfile(path):
        return
    req.urlretrieve(link, path)
    print('saved to', path)


def read_lines(path):
    with open(path) as f:
        lines = [l.strip() for l in f]
    return lines


def main():
    if not os.path.isdir(DST_DIR_PATH):
        os.makedirs(DST_DIR_PATH)

    pool = ThreadPool(N_WORKERS)
    links = read_lines(SRC_PATH)
    pool.map(download, links)

    print('saved all to', DST_DIR_PATH)


if __name__ == '__main__':
    main()
