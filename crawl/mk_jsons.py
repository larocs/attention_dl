import pubmd
import json
import glob
import bibtexparser as bt
import os


ARXIV_DATA_DIR_PATH = './arxiv_pubs/arxiv_papers_infos'
SOURCES = [
    'dblp',
    'msai',
    'deepmind',
    'googleai',
    #'openai',
    'fbai',
    'amazon',
]
BIBTEXES_PATHS = {k: './bibtexes/{}.bib'.format(k) for k in SOURCES}
DST_DIR_PATH = './pubs/jsons'


def load_bibtex(path):
    try:
        with open(path) as f:
            bib_str = f.read()
        bib_str = bib_str.lower().replace('(conference)', '')
        bib = bt.loads(bib_str)
        entries = bib.entries
    except Exception as e:
        print('ERROR:', str(e))
        return []
    return entries


BIBTEX_PUB_TYPES = {
    'article',
    'inproceedings',
    'misc',
}


def load_bibtex_data():
    data = []
    for source, path in BIBTEXES_PATHS.items():
        entries = load_bibtex(path)
        entries = [e for e in entries if e['ENTRYTYPE'] in BIBTEX_PUB_TYPES]
        for e in entries:
            e['source'] = source
        print('for source {}, loaded {} entries'.format(source, len(entries)))
        data.extend(entries)
    return data


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def load_arxiv_data():
    paths = glob.glob(os.path.join(ARXIV_DATA_DIR_PATH, '*.json'))
    data = [load_json(p)['result'] for p in paths]
    return data


def get_path(metadata):
    uid = metadata.uid
    for c in [':', '/', '.', ',', '_']:
        uid = uid.replace(c, '-')
    filename = '{}_{}.json'.format(metadata.source, uid)
    path = os.path.join(DST_DIR_PATH, filename)
    return path


def get_metadata_and_save(data_coll, cls):
    for i, data in enumerate(data_coll):
        try:
            metadata = cls.from_dict(data)
            path = get_path(metadata)
            save_json(path, metadata.as_dict())
            #print('saved md {} to {}'.format(metadata.uid, path))
        except Exception as e:
            print('ERROR in data #{}/{}: {}'.format(i+1, len(data_coll), e))
            continue


def main():
    if not os.path.isdir(DST_DIR_PATH):
        os.makedirs(DST_DIR_PATH)

    get_metadata_and_save(load_arxiv_data(), pubmd.ArxivMetadata)
    get_metadata_and_save(load_bibtex_data(), pubmd.BibtexMetadata)


if __name__ == '__main__':
    main()
