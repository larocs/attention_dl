'''
This script pre-processes papers metadata extracted from Zotero.
It formats some fields and includes others.
'''


import os
import RISparser as rp
from collections import defaultdict
import random
import hashlib

import util
import config as cfg


rp.LIST_TYPE_TAGS = tuple(rp.LIST_TYPE_TAGS + ("UR",))

def load_ris(path):
    with open(path) as f:
        entries = rp.readris(f)
    entries = list(entries)
    return entries


def _set_default_values(meta, keys, def_val=''):
    for k in keys:
        meta[k] = meta.get(k, def_val)
    return meta


def set_default_values(metas):
    keys = set(util.flatten(m.keys() for m in metas))
    for meta in metas:
        meta = _set_default_values(meta, keys)
    return metas


def set_lowercase_keys(meta):
    keys = list(meta.keys())
    for k in keys:
        if not k.islower():
            meta[k.lower()] = meta[k]
            del meta[k]
    return meta


def set_uid(meta):
    hash_obj = hashlib.sha1(str(sorted(meta.items())).encode('utf-8'))
    meta['uid'] = hash_obj.hexdigest()
    return meta


def set_local_pdf_path_field(meta):
    keys = sorted(k for k in meta.keys() if k.startswith('file_attachments'))
    for k in keys:
        if meta[k].lower().endswith('.pdf'):
            path = os.path.join(cfg.paths['exported-metadata-dir'], meta[k])
            break
    else:
        path = ''
    meta['pdf-path'] = path
    return meta


def normalize_title(meta):
    meta['norm-title'] = util.normalize_title(meta['title'])
    return meta


def normalize_authors(meta):
    authors = {util.normalize_author(a) for a in meta['authors']}
    meta['norm-authors'] = sorted(authors)
    return meta


def pre_proc_paper_meta(meta):
    meta = set_uid(meta)
    meta = set_lowercase_keys(meta)
    meta = normalize_title(meta)
    meta = normalize_authors(meta)
    meta = set_local_pdf_path_field(meta)
    return meta


def mk_unique_norm_titles(metas):
    hist = defaultdict(int)
    for meta in metas:
        hist[meta['norm-title']] += 1
        if hist[meta['norm-title']] > 1:
            new_title = '{}-{}'.format(
                meta['norm-title'], hist[meta['norm-title']])
            print('WARNING: "{}" already exists, renaming to "{}"'.format(
                meta['norm-title'], new_title))
            meta['norm-title'] = new_title
    return metas


def _pre_proc_paper_metas(metas):
    metas = set_default_values(metas)
    metas = [pre_proc_paper_meta(m) for m in metas]
    metas = mk_unique_norm_titles(metas)
    # assert len(metas) == len({m['uid'] for m in metas})
    return metas


def pre_proc_papers_metas():
    raw_metas = load_ris(cfg.paths['raw-papers-metadata'])
    metas = _pre_proc_paper_metas(raw_metas)
    util.save_json(cfg.paths['papers-metadata'], metas)
    print('saved updated papers metadata to "{}"'.format(
        cfg.paths['papers-metadata']))


def main():
    pre_proc_papers_metas()


if __name__ == '__main__':
    main()
