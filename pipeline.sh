#!/bin/bash

set -ox

python3 ./pre_proc_papers_metadata.py

python3 ./download_missing_paper_pdfs.py

python3 ./extract_raw_refs_from_pdfs.py
python3 ./parse_raw_refs.py

python3 ./mk_citation_graphs.py
python3 ./mk_histograms.py

python3 ./plot_histograms.py
python3 ./plot_graphs.py
