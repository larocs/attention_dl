'''
Makes citation graphs for authors and titles, in the style of:
    - author: {authors cited by author in collection of papers}
    - author: {authors that cite author in collection of papers}
    - title: {titles cited by title in collection of papers}
    - title: {titles that cite title in collection of papers}
'''


from functools import reduce

import util
import config as cfg


def get_all_nodes(graph):
    all_nodes = set(graph.keys())
    #all_nodes |= reduce(lambda a, b: set(a) | set(b), graph.values(), set())
    return all_nodes


def get_rev_graph(graph):
    all_nodes = get_all_nodes(graph)
    rev_graph = {node: set() for node in all_nodes}
    for to_node in all_nodes:
        for from_node, nodes in graph.items():
            if to_node in nodes and from_node in all_nodes:
                rev_graph[to_node].add(from_node)
    return rev_graph


# def get_title_refs_graph(metas, refs):
#     all_titles = {m['norm-title'] for m in metas}
#     graph = {}
#     for meta in metas:
#         refs_ = refs.get(meta['uid'], [])
#         cited_titles = {r['norm-title'] for r in refs_}
#         cited_titles &= all_titles
#         graph[meta['norm-title']] = cited_titles
#     return graph

############

# from difflib import SequenceMatcher


# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()


def get_title_refs_graph(metas, refs):
    for m in metas:
        m['title'] = util.normalize_title(m['title'])
    all_titles = {m['title'] for m in metas}
    graph = {}
    for meta in metas:
        refs_ = refs.get(meta['uid'], [])
        cited_titles = []
        for ref in refs_:
            if ref:
                cited_titles.append(util.normalize_title(ref[0]))
        cited_titles = set(cited_titles)
        # for ctitle in cited_titles:
        #     for atitle in all_titles:
        #         sim = similar(
        #             ctitle,
        #             atitle
        #         )
        #         if sim > 0.8:
        #             print(sim)
        #             print(ctitle)
        #             print(atitle)
        #             import pdb; pdb.set_trace()
        cited_titles &= all_titles
        graph[meta['title']] = cited_titles
    return graph


# def get_author_refs_graph(metas, refs):
#     all_titles = {m['norm-title'] for m in metas}
#     all_authors = set(util.flatten(m['norm-authors'] for m in metas))
#     graph = {a: set() for a in all_authors}
#     for meta in metas:
#         refs_ = refs.get(meta['uid'], [])
#         refs_ = [r for r in refs_ if r['norm-title'] in all_titles]
#         cited_authors = set(util.flatten(r['norm-authors'] for r in refs_))
#         cited_authors &= all_authors
#         for a in meta['norm-authors']:
#             graph[a] |= cited_authors
#     return graph


def get_author_refs_graph(metas, refs):
    return {}


def mk_citation_graphs():
    metas = util.load_json(cfg.paths['papers-metadata'])
    refs = util.load_json(cfg.paths['papers-refs'])

    graph = get_title_refs_graph(metas, refs)
    util.save_graph(cfg.paths['titles-refs-graph'], graph)
    print('saved titles refs graph to "{}"'.format(
        cfg.paths['titles-refs-graph']))

    rev_graph = get_rev_graph(graph)
    util.save_graph(cfg.paths['titles-refs-rev-graph'], rev_graph)
    print('saved reversed titles refs graph to "{}"'.format(
        cfg.paths['titles-refs-rev-graph']))

    graph = get_author_refs_graph(metas, refs)
    util.save_graph(cfg.paths['authors-refs-graph'], graph)
    print('saved authors refs graph to "{}"'.format(
        cfg.paths['authors-refs-graph']))

    rev_graph = get_rev_graph(graph)
    util.save_graph(cfg.paths['authors-refs-rev-graph'], rev_graph)
    print('saved reversed authors refs graph to "{}"'.format(
        cfg.paths['authors-refs-rev-graph']))


def main():
    mk_citation_graphs()


if __name__ == '__main__':
    main()
