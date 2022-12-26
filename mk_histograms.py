'''
Produces the following set of histograms:
    - word count for all abstracts/titles in papers
    - title/author citation count
'''


from nltk.corpus import stopwords
from collections import defaultdict

import util
import config as cfg


#stopwords, ie, words to not be considered in counting
try:
    STOPWORDS = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    STOPWORDS = set(stopwords.words('english'))
STOPWORDS |= {
    'via',
    'propose',
    'proposed',
    'paper',
    'also',
}
#normalize histogram frequencies
NORM_HIST = False
#gets only words >= percentile
PERCENTILE = None


def norm_hist(hist):
    total = sum(hist.values())
    hist = {k: v/max(total, 1) for k, v in hist.items()}
    return hist


def crop_hist_by_percentile(hist, percentile):
    hist = list(hist.items())
    hist.sort(key=lambda kv: kv[1], reverse=True)
    perc = np.percentile([v for __, v in hist], percentile)
    hist = {k: v for k, v in hist if v >= perc}
    return hist


def get_words_hist(words):
    hist = defaultdict(int)
    for w in words:
        hist[w] += 1
    hist = {w: f for w, f in hist.items() if w not in STOPWORDS}
    return hist


def get_citations_hist(graph):
    '''
    Assumes graph in format author: {authors citing author}
    '''
    hist = {k: len(v) for k, v in graph.items()}
    return hist


def get_words(text):
    words = util.slugify(text).split('-')
    words = [w for w in words if w]
    return words


def get_all_words(metas, key):
    words = []
    for meta in metas:
        text = meta.get(key, '')
        words.extend(get_words(text))
    return words


def plot_words(hist, max_n_words=None, term=None):
    #converting word freq hist to sorted list of words and frequencies
    words_freqs = sorted(hist.items(), key=lambda kv: kv[1], reverse=True)
    words_freqs = words_freqs[slice(max_n_words)]
    words, freqs = map(list, zip(*words_freqs))
    x = list(range(len(words)))
    #plotting
    fig, ax = plt.subplots()
    ax.barh(x, freqs, align='center')
    #title/labels
    ax.set_yticks(x)
    ax.set_yticklabels(words)
    ax.invert_yaxis()
    if term is not None:
        ax.set_title('word frequencies in {} (top {})'.format(term, len(x)))
    ax.set_ylabel('word')
    ax.set_xlabel('frequency')
    #proper plot size
    height = np.ceil((max_n_words/64)*11)
    fig.set_size_inches((11, height), forward=False)
    return fig


def get_word_freqs(metas, term, norm=False, percentile=None):
    #getting all words
    words = get_all_words(metas, term)
    #getting word freq histogram
    hist = get_words_hist(words)
    if percentile is not None:
        hist = crop_hist_by_percentile(hist, percentile)
    if norm:
        hist = norm_hist(hist)

    #saving .csv with frequencies
    lines = sorted(hist.items(), key=lambda kv: kv[1], reverse=True)
    lines = ['{},{}'.format(w, f) for w, f in lines]
    util.save_lines(cfg.paths['{}-word-freq-csv'.format(term)], lines)
    print('saved .csv with all word freqs for "{}" to "{}"'.format(
        term, cfg.paths['{}-word-freq-csv'.format(term)]))


def mk_word_freq_hists(norm=False, percentile=None):
    metas = util.load_json(cfg.paths['papers-metadata'])
    for term in ['abstract', 'title']:
        words = get_all_words(metas, term)
        hist = get_words_hist(words)
        if percentile is not None:
            hist = crop_hist_by_percentile(hist, percentile)
        if norm:
            hist = norm_hist(hist)
        path = cfg.paths['{}-word-freqs-hist'.format(term)]
        util.save_csv_hist(path, hist)
        print('saved .csv word freq hist for "{}" to "{}"'.format(term, path))


def mk_citation_hists(norm=False, percentile=None):
    for term in ['authors', 'titles']:
        graph = util.load_json(cfg.paths['{}-refs-rev-graph'.format(term)])
        hist = get_citations_hist(graph)
        path = cfg.paths['{}-refs-hist'.format(term)]
        util.save_csv_hist(path, hist)
        print('saved .csv citations hist for "{}" to "{}"'.format(term, path))


def mk_histograms():
    mk_word_freq_hists()
    mk_citation_hists()


def main():
    mk_histograms()


if __name__ == '__main__':
    main()
