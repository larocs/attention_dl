'''
Plots occurrences of attention-themed papers over years.
An attention-themed paper is defined as a paper with either
"attention", "attentive" or "attentional" in the title.
'''


import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
style.use('seaborn')
import glob

import util
import config as cfg


def plot_occurrences(years, freqs, venue, percentage=False):
    #plotting
    fig, ax = plt.subplots()
    ax.bar(years, freqs, align='center')
    title = '{}: {} of attention-themed papers over years'.format(
        venue, 'percentage' if percentage else 'number')
    ax.set_title(title)
    ax.set_xlabel('year')
    ax.set_ylabel('percentage' if percentage else 'frequency')
    #proper plot size
    plt.tight_layout()
    #plt.show()
    return fig


def get_plot_path(venue, percentage=False):
    filename = '{}_freqs-over-years{}.pdf'.format(
        venue.lower(), '_percentage' if percentage else '')
    return os.path.join(cfg.paths['occurrences-over-years-plots-dir'], filename)


def plot_occurrences_over_years_for_venue(df, venue):
    df = df.sort_values(by='year')
    fig = plot_occurrences(df['year'], df['n_occurrences'], venue)
    path = get_plot_path(venue)
    fig.savefig(path)
    print('saved plot for venue "{}" to {}'.format(venue, path))
    if 'total_n_papers' in df.columns:
        fig = plot_occurrences(
            df['year'], 100*df['n_occurrences']/df['total_n_papers'], venue,
            percentage=True)
        path = get_plot_path(venue, percentage=True)
        fig.savefig(path)
        print('saved plot for venue "{}" (percentage) to {}'.format(
            venue, path))


def plot_occurrences_over_years():
    paths = glob.glob(
        os.path.join(cfg.paths['occurrences-over-years-data-dir'], '*.csv'))
    if not paths:
        print('dir "{}" for n. of attention-themed papers over the years '
            'not found or no CSV files found in dir'.format(
            cfg.paths['occurrences-over-years-data-dir']))
        return
    for path in paths:
        venue = os.path.basename(path).rstrip('.csv').split('_')[0].upper()
        df = pd.read_csv(path)
        plot_occurrences_over_years_for_venue(df, venue)


def main():
    plot_occurrences_over_years()


if __name__ == '__main__':
    main()
