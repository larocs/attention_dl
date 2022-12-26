'''
Plots previously produced histograms (word/citation count) for visualization.
'''


from matplotlib import pyplot as plt
from matplotlib import style
style.use('seaborn')
import numpy as np

import util
import config as cfg


#maximum number of words to use in plot. can be None
MAX_N_TERMS = 100
#plot size in format width, height
DEF_PLOT_SHAPE = (11, 12)
#default plot color
DEF_COLOR = 'orange'


def get_plot_shape(terms):
    n = len(terms)
    def_w, def_h = DEF_PLOT_SHAPE
    h = int(np.ceil(def_h*n/64))
    term_size_perc = np.ceil(np.percentile([len(t) for t in terms], 95))
    w = def_w + int(np.ceil(term_size_perc/8))
    return w, h


def plot_hist(hist, max_n_terms=None, title=None):
    #converting word freq hist to sorted list of words and frequencies
    terms_freqs = sorted(hist.items(), key=lambda kv: kv[1], reverse=True)
    terms_freqs = terms_freqs[slice(max_n_terms)]
    terms, freqs = map(list, zip(*terms_freqs))
    x = list(range(len(terms)))
    #plotting
    fig, ax = plt.subplots()
    ax.barh(x, freqs, align='center', color=DEF_COLOR)
    #title/labels
    ax.set_yticks(x)
    ax.set_yticklabels(terms)
    ax.invert_yaxis()
    if title is not None:
        ax.set_title(title)
    ax.set_ylabel('term')
    ax.set_xlabel('frequency')
    #proper plot size
    plot_shape = get_plot_shape(terms)
    fig.set_size_inches(plot_shape, forward=False)
    plt.tight_layout()
    return fig


def plot_words_freqs(hist, term, max_n_words=None, savefig_dpi=300):
    title = 'word frequencies in papers "{}" part'.format(term)
    fig = plot_hist(hist, max_n_terms=max_n_words, title=title)
    path = cfg.paths['{}-word-freqs-hist-plot'.format(term)]
    fig.savefig(path, dpi=savefig_dpi)
    print('saved word freq plot for "{}" to "{}"'.format(term, path))


def plot_citations_freqs(hist, term, max_n_terms=None, savefig_dpi=300):
    title = '{} citations frequencies in papers'.format(term)
    fig = plot_hist(hist, max_n_terms=max_n_terms, title=title)
    path = cfg.paths['{}-refs-hist-plot'.format(term)]
    fig.savefig(path, dpi=savefig_dpi)
    print('saved citation hist plot for "{}" to "{}"'.format(term, path))


def plot_histograms():
    for term in 'title', 'abstract':
        hist = util.load_csv_hist(cfg.paths['{}-word-freqs-hist'.format(term)])
        plot_words_freqs(hist, term, max_n_words=MAX_N_TERMS)
    for term in 'authors', 'titles':
        hist = util.load_csv_hist(cfg.paths['{}-refs-hist'.format(term)])
        plot_citations_freqs(hist, term, max_n_terms=MAX_N_TERMS)


def main():
    plot_histograms()


if __name__ == '__main__':
    main()
