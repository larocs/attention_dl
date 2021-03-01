import requests
import json
import glob
import os
import tempfile
import re
import unicodedata
import uuid
import subprocess as sp
import multiprocessing as mp


def get_rand_str():
    return str(uuid.uuid4()).split('-')[-1]


def get_tmp_dir(prefix='litrev'):
    path = os.path.join(
        tempfile.gettempdir(), '{}-{}'.format(prefix, get_rand_str()))
    os.makedirs(path)
    return path


def get_tmp_file(filename=None, suffix=None):
    if filename is None:
        filename = get_rand_str()
    if suffix is not None:
        filename = filename + suffix
    path = os.path.join(tempfile.gettempdir(), filename)
    return path


def download(url, dst_path):
    with open(dst_path, 'w') as f:
        resp = requests.get(url)
        f.write(str(resp.content))
    return dst_path


def flatten(iterable):
    return (item for subiterable in iterable for item in subiterable)


def slugify(seq, sep='-'):
    seq = unicodedata.normalize('NFKD', seq)
    seq = seq.encode('ascii', 'ignore').decode()
    seq = seq.strip().lower()
    seq = re.sub(r'[^\w\s-]', '', seq)
    seq = re.sub(r'[-\s]+', sep, seq)
    return seq


def remove(string, seqs):
    for seq in seqs:
        string = string.replace(seq, '')
    return string


def remove_reps(string, char):
    assert len(char) == 1
    while 2*char in string:
        string = string.replace(2*char, char)
    return string


def read_lines(path):
    with open(path) as f:
        lines = [l.strip() for l in f]
    return lines


def save_lines(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            print(line, file=f)
    return path


def load_json(path):
    with open(path) as f:
        dct = json.load(f)
    return dct


def load_graph(path):
    graph = load_json(path)
    graph = {k: set(v) for k, v in graph.items()}
    return graph


def save_graph(path, graph):
    graph = {k: list(v) for k, v in graph.items()}
    save_json(path, graph)
    return path


def save_json(path, dct):
    with open(path, 'w') as f:
        json.dump(dct, f, indent=4, sort_keys=True)


def get_info_fn(prefix='', def_flush=True, silence=False):
    def wrapper(*args, **kwargs):
        if not 'flush' in kwargs:
            kwargs['flush'] = def_flush
        if not silence:
            print(prefix, *args, **kwargs)
    return wrapper


def run_cmd(cmd, check=True, **kwargs):
    print('cmd:', cmd)
    proc = sp.run(cmd, check=check, **kwargs)
    return proc


def parallelize(fn, args, n_threads=1, star=False):
    pool = mp.Pool(n_threads)
    if star:
        ret = pool.starmap(fn, args)
    else:
        ret = pool.map(fn, args)
    return ret


_CSV_HIST_HEADER = 'term,frequency'


def save_csv_hist(path, hist, sort_by_freqs=True):
    items = list(hist.items())
    if sort_by_freqs:
        items.sort(key=lambda kv: kv[1], reverse=True)
    lines = [_CSV_HIST_HEADER]
    lines.extend('{},{}'.format(k, v) for k, v in items)
    save_lines(path, lines)


def load_csv_hist(path):
    lines = read_lines(path)
    if lines and lines[0] == _CSV_HIST_HEADER:
        lines = lines[1:]
    items = [l.split(',') for l in lines]
    hist = {k: (float if '.' in v else int)(v) for k, v in items}
    return hist


#maximum number of names that are not last names to be used. can be None
DEF_MAX_N_NONLAST_NAMES = 0


def crop_author_names(author, max_n_nonlast_names=DEF_MAX_N_NONLAST_NAMES):
    '''
    Assumes author comes pre-processed:
    Slugified (separated by hyphens), without numbers, punctiation chars.
    '''
    tokens = author.split('-')
    #using only first letter for names that are not last name
    tokens[:-1] = [tok[:1] for tok in tokens[:-1]]
    #selecting last name and limit number of nonlast names
    if max_n_nonlast_names is not None and len(tokens) > 1:
        assert max_n_nonlast_names >= 0
        tokens = tokens[:-1][:max_n_nonlast_names] + [tokens[-1]]
    return '-'.join(tokens)


def pre_proc_author(author):
    '''
    Assumes author comes from raw text strings from ref file/paper metadata.
    '''
    #removing numbers, trailing spaces and repeating spaces
    author = remove(author, '0123456789')
    author = author.strip(' ')
    author = remove_reps(author, ' ')
    #if there's a comma, assumes it's in format 'last name, blablabla'
    if ',' in author:
        if author.count(',') > 1:
            print('WARNING: more than one comma in "{}"'.format(author))
        author = ' '.join(author.split(',')[::-1])
    #assuming there are names that use hyphen and can be separated by spaces
    author = author.replace('-', ' ')
    #transforming to lowercase slugified format
    author = slugify(author, sep='-')
    return author


def normalize_author(author):
    author = pre_proc_author(author)
    author = crop_author_names(author)
    return author


def normalize_title(title):
    '''
    Assumes title comes from raw text strings from ref file/paper metadata.
    '''
    title = '' if title is None else title
    title = title.lower()
    #removing numbers
    title = remove(title, '0123456789')
    #using only first sentenced that ends with punctuation
    title = title.split('.')[0]
    #slugifying
    title = slugify(title)
    #removing polluting items
    tokens = title.split('-')
    for term in ['et', 'al']:
        tokens = [tok for tok in tokens if not tok == term]
    for term in ['arxiv', 'biorxiv', 'preprint', 'abs/']:
        tokens = [tok for tok in tokens if not tok.startswith(term)]
    for term in ['/']:
        tokens = [tok for tok in tokens if not term in tok]
    title = '-'.join(tokens)
    return title


def mk_dir_if_needed(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def mk_dirname_if_needed(path):
    mk_dir_if_needed(os.path.dirname(path))
