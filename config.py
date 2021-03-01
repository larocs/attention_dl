import os


#path to this file
_file_path = os.path.abspath(__file__)
_file_dir = os.path.dirname(_file_path)

#paths dictionary with paths that are common to many scripts
paths = {
    #main data directory path
    'data-dir': os.path.join(_file_dir, 'data'),
}
if not os.path.isdir(paths['data-dir']):
    os.makedirs(paths['data-dir'])

#metadata exported by zotero (with pdfs copied and .ris file produced)
paths['exported-metadata-dir'] = os.path.join(
    paths['data-dir'], 'zotero-exported-items')
paths['raw-papers-metadata'] = os.path.join(
    paths['exported-metadata-dir'], 'zotero-exported-items.ris')

#pre-processed papers metadata based on zotero exported metadata
paths['papers-metadata'] = os.path.join(
    paths['data-dir'], 'papers-metadata.json')

#directory for downloaded pdfs that weren't present in exported metadata
paths['pdfs-dir'] = os.path.join(paths['data-dir'], 'pdfs')

#raw references file produced by analyzing papers pdfs
paths['raw-papers-refs'] = os.path.join(
    paths['data-dir'], 'papers-raw-refs.json')
#parsed raw references
paths['papers-refs'] = os.path.join(
    paths['data-dir'], 'papers-refs.json')

#authors citations graph in format {author: {authors cited by author}}
paths['authors-refs-graph'] = os.path.join(
    paths['data-dir'], 'authors-refs-graph.json')
#authors citations graph in format {author: {authors that cited author}}
paths['authors-refs-rev-graph'] = os.path.join(
    paths['data-dir'], 'authors-refs-rev-graph.json')

#paper titles refs graph in format {title: {titles cited by paper}}
paths['titles-refs-graph'] = os.path.join(
    paths['data-dir'], 'titles-refs-graph.json')
#paper titles refs graph in format {title: {titles that cited paper}}
paths['titles-refs-rev-graph'] = os.path.join(
    paths['data-dir'], 'titles-refs-rev-graph.json')

#histograms for word frequencies in papers titles
paths['title-word-freqs-hist'] = os.path.join(
    paths['data-dir'], 'title-word-freqs-hist.csv')
#histograms for word frequencies in papers abstracts
paths['abstract-word-freqs-hist'] = os.path.join(
    paths['data-dir'], 'abstract-word-freqs-hist.csv')
#histograms for author citations ocurrences
#in format {author: n. of authors that cite author}
paths['authors-refs-hist'] = os.path.join(
    paths['data-dir'], 'authors-refs-hist.csv')
#histograms for paper title citations ocurrences
#in format {title: n. of papers that cite title}
paths['titles-refs-hist'] = os.path.join(
    paths['data-dir'], 'titles-refs-hist.csv')

#plots for histograms
paths['title-word-freqs-hist-plot'] = os.path.join(
    paths['data-dir'], 'title-word-freqs-hist.pdf')
paths['abstract-word-freqs-hist-plot'] = os.path.join(
    paths['data-dir'], 'abstract-word-freqs-hist.pdf')
paths['authors-refs-hist-plot'] = os.path.join(
    paths['data-dir'], 'authors-refs-hist.pdf')
paths['titles-refs-hist-plot'] = os.path.join(
    paths['data-dir'], 'titles-refs-hist.pdf')

#plots for graphs
paths['titles-graph-plot'] = os.path.join(
    paths['data-dir'], 'titles-graph.pdf')
paths['authors-graph-plot'] = os.path.join(
    paths['data-dir'], 'authors-graph.pdf')
#mapping used in graph plots
paths['titles-graph-plot-mapping'] = os.path.join(
    paths['data-dir'], 'titles-graph-plot-mapping.json')
paths['authors-graph-plot-mapping'] = os.path.join(
    paths['data-dir'], 'authors-graph-plot-mapping.json')

#dir to get data of occurences over years
paths['occurrences-over-years-data-dir'] = os.path.join(
    paths['data-dir'], 'attention-themed-papers-over-years')
paths['occurrences-over-years-plots-dir'] = paths['data-dir']

#path to script that extracts raw references strings from pdfs
extract_refs_script_path = os.path.join(_file_dir, 'extractrefs.py')

#path to dir to save pubs search results
paths['search-pubs-results-dir'] = os.path.join(
    paths['data-dir'], 'search-pubs-results')

#number of threads to use on scripts that use parallelism
n_threads = 8
