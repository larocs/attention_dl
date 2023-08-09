#!/bin/bash

set -ox

python ./pre_proc_papers_metadata.py

python ./download_missing_paper_pdfs.py

python ./extract_raw_refs_from_pdfs.py
python ./parse_raw_refs.py

python ./mk_citation_graphs.py
python ./mk_histograms.py

python ./plot_histograms.py
python ./plot_graphs.py
