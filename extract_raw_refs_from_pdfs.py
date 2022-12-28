'''
Extracts references from pdf files.
'''


import util
import config as cfg
import json
from refextract import extract_references_from_file, extract_references_from_url


#script config
N_THREADS = cfg.n_threads


def _extract_refs(pdf_path, dst_path):
    assert pdf_path.endswith('.pdf')

    if pdf_path.startswith('http://') or pdf_path.startswith('https://'):
        # refs = refextract.extract_references_from_url(pdf_path)
        refs = extract_references_from_url(pdf_path)
    else:
        # refs = refextract.extract_references_from_file(pdf_path)
        print(pdf_path)
        refs = extract_references_from_file(pdf_path)

    with open(dst_path, 'w') as f:
        json.dump(refs, f, indent=4)
    print('saved refs to %s' % dst_path)


def extract_refs(src_path):
    #it's necessary to wrap the script because the lib is in python2.7
    dst_path = util.get_tmp_file(suffix='.json')
    # util.run_cmd([
    #     cfg.extract_refs_script_path,
    #     src_path,
    #     dst_path,
    # ])
    _extract_refs(src_path, dst_path)
    refs = util.load_json(dst_path)
    return refs


def extract_raw_refs_from_pdf(meta):
    print('on paper "{}"'.format(meta['norm-title']))
    try:
        refs = extract_refs(meta['pdf-path'])
    except Exception as e:
        print('ERROR on paper "{}": "{}"'.format(
            meta['norm-title'], e))
        refs = []
    # refs = [r.get('raw_ref', '') for r in refs]
    refs = [
        r.get('title', '') for r in refs
    ]
    return refs


def extract_raw_refs_from_pdfs():
    metas = util.load_json(cfg.paths['papers-metadata'])
    refs = util.parallelize(extract_raw_refs_from_pdf, metas, N_THREADS)
    refs = {m['uid']: r for m, r in zip(metas, refs)}
    util.save_json(cfg.paths['raw-papers-refs'], refs)

    print('saved raw papers refs to "{}"'.format(cfg.paths['raw-papers-refs']))


def main():
    extract_raw_refs_from_pdfs()


if __name__ == '__main__':
    main()
