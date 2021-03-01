#!/usr/bin/env python3


'''
Downloads pdf files from papers metadata file.
'''


import os
import requests

import util
import config as cfg


#script config
N_THREADS = cfg.n_threads


def get_local_pdf_path(meta, pdfs_dir_path):
    filename = '{}_{}.pdf'.format(meta['norm-title'], meta['uid'])
    path = os.path.join(pdfs_dir_path, filename)
    return path


def get_paper_pdf_url(url):
    meta = requests.utils.urlparse(url)
    if url.lower().endswith('.pdf'):
        pdf_url = url
    elif meta.netloc == 'arxiv.org':
        uid = meta.path.split('/')[-1]
        url = '{}://arxiv.org/pdf/{}.pdf'.format(meta.scheme, uid)
    else:
        raise ValueError('could not get pdf url for "{}"'.format(url))
    return url


def download_paper_pdf_if_needed(meta):
    info = util.get_info_fn('[{}] '.format(meta['title']))

    if os.path.isfile(meta['pdf-path']):
        info('file "{}" already exists, exitting'.format(meta['pdf-path']))
        return meta
    try:
        url = get_paper_pdf_url(meta['url'])
    except ValueError:
        info('ERROR: could not get pdf url for paper url "{}"'.format(
            meta['url']))
        return meta
    try:
        path = get_local_pdf_path(meta, cfg.paths['pdfs-dir'])
        info('downloading pdf from "{}"'.format(url))
        util.download(url, path)
        meta['pdf-path'] = path
    except Exception as e:
        info('ERROR downloading pdf: "{}"'.format(e))

    return meta


def download_missing_paper_pdfs():
    if not os.path.isdir(cfg.paths['pdfs-dir']):
        os.makedirs(cfg.paths['pdfs-dir'])

    metas = util.load_json(cfg.paths['papers-metadata'])
    metas = util.parallelize(download_paper_pdf_if_needed, metas, N_THREADS)
    util.save_json(cfg.paths['papers-metadata'], metas)

    print('\n----')
    print('saved updated papers metadata to "{}"'.format(
        cfg.paths['papers-metadata']))
    n = sum(int(os.path.isfile(m['pdf-path'])) for m in metas)
    print('{}/{} ({:.3f}%) items with pdfs'.format(
        n, len(metas), 100*n/len(metas)))


def main():
    download_missing_paper_pdfs()


if __name__ == '__main__':
    main()
