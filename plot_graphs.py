#!/usr/bin/env python3


'''
Plots reference graphs for authors and titles.
'''


import networkx as nx
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib import style
style.use('seaborn')
import random
import math

import util
import config as cfg


#maximum number of nodes to plot. will select the most cited nodes
MAX_N_AUTHOR_NODES = 64
MAX_N_TITLE_NODES = 48
#relabel titles/authors to use number instead of the title
RELABEL_TITLES = False
RELABEL_AUTHORS = False
#graph drawing layouts to be tried in preference order
PREFERRED_LAYOUTS = [
    lambda g: nx.drawing.nx_pydot.graphviz_layout(g, prog='neato'),
    lambda g: nx.drawing.kamada_kawai_layout(g),
    lambda g: nx.drawing.shell_layout(g),
    lambda g: None,
]


def get_savefig_size(n_nodes):
    size = math.ceil(20*(n_nodes/24)**0.5)
    return (size, size)


def get_nx_graph(graph):
    nx_graph = nx.DiGraph()
    for u, vs in graph.items():
        nx_graph.add_edges_from([(u, v) for v in vs])
    return nx_graph


def get_graph(nx_graph):
    graph = {n: set() for n in nx_graph.nodes()}
    for u, v in nx_graph.edges():
        graph[u].add(v)
    return graph


def filter_graph(graph, nodes):
    nodes = set(nodes)
    graph = {k: v for k, v in graph.items() if k in nodes}
    graph = {k: {v_ for v_ in v if v_ in nodes} for k, v in graph.items()}
    return graph


def get_all_nodes(graph):
    all_nodes = set(graph.keys()) | set(util.flatten(graph.values()))
    return all_nodes


def select_nodes(nodes, hist, max_n_nodes=None):
    nodes = sorted(nodes, key=lambda n: hist.get(n, 0), reverse=True)
    nodes = set(nodes[slice(max_n_nodes)])
    return nodes


def reduce_graph(graph, hist, max_n_nodes=None):
    all_nodes = get_all_nodes(graph)
    nodes = select_nodes(all_nodes, hist, max_n_nodes)
    graph = filter_graph(graph, nodes)
    return graph


def relabel_graph(graph, mapping=None):
    if mapping is None:
        mapping = {k: i for i, k in enumerate(get_all_nodes(graph))}
    graph = {k: {mapping[v_] for v_ in v} for k, v in graph.items()}
    graph = {mapping[k]: v for k, v in graph.items()}
    return graph, mapping


def get_def_dict(dct, typ):
    new_dct = defaultdict(typ)
    for k, v in dct.items():
        new_dct[k] = v
    return new_dct


def relabel_hist(hist, mapping):
    new_hist = {}
    for k, v in mapping.items():
        new_hist[v] = hist.get(k, 0)
    new_hist = get_def_dict(new_hist, int)
    return new_hist


def unit_norm_hist(hist):
    minn = min(hist.values())
    maxx = max(hist.values())
    hist = {k: (v - minn)/(maxx - minn) for k, v in hist.items()}
    hist = get_def_dict(hist, float)
    return hist


def get_node_sizes(nx_graph, hist):
    hist = unit_norm_hist(hist)
    nodes = list(nx_graph.nodes())
    sizes = [int(128 + 4096*hist[n]) for n in nodes]
    return sizes


def get_plot_layout(nx_graph, layouts=PREFERRED_LAYOUTS):
    for fn in layouts:
        try:
            layout = fn(nx_graph)
            return layout
        except Exception as e:
            print('WARNING: could not get layout: "{}". trying next'.format(e))
    raise


def get_node_colors(nx_graph):
    graph = get_graph(nx_graph)
    hist = {k: len(v) for k, v in graph.items()}
    colors = [hist[n] for n in nx_graph.nodes()]
    return colors


def plot_nx_graph(graph, hist, **kwargs):
    norm_hist = unit_norm_hist(hist)
    fig, ax = plt.subplots()
    nx.draw_networkx(
        graph,
        pos=get_plot_layout(graph),
        ax=ax,
        node_size=get_node_sizes(graph, hist),
        node_color=get_node_colors(graph),
        cmap=plt.cm.YlOrRd,
        edge_color='grey',
        arrowsize=10,
        arrowstyle='->',
        font_color='black',
        **kwargs,
    )
    if kwargs.get('title') is not None:
        ax.set_title(kwargs['title'])
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    return fig, ax


def plot_graph(graph, hist, relabel=False, max_n_nodes=None, title=None):
    graph = reduce_graph(graph, hist, max_n_nodes)
    if relabel:
        graph, mapping = relabel_graph(graph)
        hist = relabel_hist(hist, mapping)
    else:
        mapping = None
    nx_graph = get_nx_graph(graph)
    fig, ax = plot_nx_graph(nx_graph, hist,
        title='citation graph (top {} cited nodes)'.format(max_n_nodes))
    return fig, ax, mapping


def plot_titles_graph():
    graph = util.load_graph(cfg.paths['titles-refs-graph'])
    hist = util.load_csv_hist(cfg.paths['titles-refs-hist'])
    fig, ax, mapping = plot_graph(
        graph, hist, relabel=RELABEL_TITLES, max_n_nodes=MAX_N_TITLE_NODES)

    fig.set_size_inches(get_savefig_size(MAX_N_TITLE_NODES), forward=False)
    fig.savefig(cfg.paths['titles-graph-plot'], dpi=333)
    print('saved titles graph plot to "{}"'.format(
        cfg.paths['titles-graph-plot']))
    if mapping is not None:
        util.save_json(cfg.paths['titles-graph-plot-mapping'], mapping)
        print('saved titles graph plot mapping to "{}"'.format(
            cfg.paths['titles-graph-plot-mapping']))


def plot_authors_graph():
    graph = util.load_graph(cfg.paths['authors-refs-graph'])
    hist = get_def_dict(
        util.load_csv_hist(cfg.paths['authors-refs-hist']), int)
    fig, ax, mapping = plot_graph(
        graph, hist, relabel=RELABEL_AUTHORS, max_n_nodes=MAX_N_AUTHOR_NODES)

    fig.set_size_inches(get_savefig_size(MAX_N_AUTHOR_NODES), forward=False)
    fig.savefig(cfg.paths['authors-graph-plot'], dpi=333)
    print('saved authors graph plot to "{}"'.format(
        cfg.paths['authors-graph-plot']))
    if mapping is not None:
        util.save_json(cfg.paths['authors-graph-plot-mapping'], mapping)
        print('saved authors graph plot mapping to "{}"'.format(
            cfg.paths['authors-graph-plot-mapping']))


def plot_graphs():
    plot_titles_graph()
    plot_authors_graph()


def main():
    plot_graphs()


if __name__ == '__main__':
    main()
