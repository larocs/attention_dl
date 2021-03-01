# litrev - Analyze papers metadata

This set of scripts analyzes papers metadata, generating more metadata files and visualization plots.
It is supposed to work with Zotero.

## Initial setup
Dependencies:
- Python 3: they are listed on `requirements.txt`.
- Python 2: we need [refextract](https://github.com/inspirehep/refextract) and it's not available for python 3. So install it from git or use `pip2 install refextract`.
- [Zotero](https://www.zotero.org): it was tested on version `5.0.57`.

## Using the scripts
To obtain the initial data the scripts need in Zotero:
- Select a set of papers.
- Right click -> *Export Items*.
- Select RIS format and check *Export Notes* and *Export Files*.

Once you have the metadata:
- Edit `config.py` to set paths and other stuff.
- Run `./pipeline.sh` to produce all files.
