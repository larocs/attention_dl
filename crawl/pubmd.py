import json
import arrow
import pprint
import hashlib
import bibtexparser as bt


def _load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


class PubMetadata:
    FIELDS = {
        'authors',
        'title',
        'year',
        'abstract',
        'uid',
        'url',
        'source',
    }


    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError


    @classmethod
    def load(cls, path):
        raise NotImplementedError


    @property
    def title(self):
        raise NotImplementedError


    @property
    def authors(self):
        raise NotImplementedError


    @property
    def year(self):
        raise NotImplementedError


    @property
    def abstract(self):
        raise NotImplementedError


    @property
    def url(self):
        raise NotImplementedError


    @property
    def source(self):
        raise NotImplementedError


    def __hash__(self):
        return hash(
            (self.title, frozenset(self.authors), self.year, self.abstract))


    @property
    def uid(self):
        hsh = hashlib.new('ripemd160')
        seq = ''.join(
            str(getattr(self, k)) for k in PubMetadata.FIELDS - {'uid'})
        hsh.update(seq.encode())
        uid = hsh.hexdigest()[:40]
        return uid


    def as_dict(self):
        return {k: getattr(self, k) for k in self.__class__.FIELDS}


    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__, pprint.pformat(self.as_dict()))



class ArxivMetadata(PubMetadata):
    @classmethod
    def from_dict(cls, data):
        '''
        Assumes data is a dict with at least the keys
        abstract, arxiv_id, submission_date, title, authors (a list)
        '''
        if 'result' in data:
            data = data['result']
        return ArxivMetadata(
            title=data['title'],
            authors=data['authors'],
            submission_date=data['submission_date'],
            arxiv_id=data['arxiv_id'],
            abstract=data['abstract'],
        )


    @classmethod
    def load(cls, path):
        data = _load_json(path)
        return cls.from_dict(data)


    def __init__(self, title, authors, submission_date, arxiv_id, abstract):
        self._title = title
        self._authors = authors
        self._submission_date = submission_date
        self._arxiv_id = arxiv_id
        self._abstract = abstract


    @property
    def title(self):
        return self._title.lower()


    @property
    def authors(self):
        return [a.lower() for a in self._authors]


    @property
    def year(self):
        return arrow.get(self._submission_date).date().year


    @property
    def abstract(self):
        return self._abstract.lower()


    @property
    def uid(self):
        return 'arxiv:' + self._arxiv_id


    @property
    def url(self):
        return 'https://arxiv.org/abs/{}'.format(self._arxiv_id)


    @property
    def source(self):
        return 'arxiv'


def _parse_bibtex_authors(text):
    text = text.lower()
    authors = text.split('and')
    authors = [a.strip('\n ') for a in authors]
    return authors


class BibtexMetadata(PubMetadata):
    @classmethod
    def from_dict(cls, data):
        return BibtexMetadata(
            title=data['title'],
            author=data['author'],
            year=data.get('year'),
            abstract=data.get('abstract'),
            doi=data.get('doi'),
            url=data.get('url'),
            source=data.get('source'),
        )


    _PUB_TYPES = {
        'inproceedings',
        'article',
    }


    @classmethod
    def load(cls, path):
        with open(path) as f:
            bib_str = f.read()
        bib_str = bib_str.lower().replace('(conference)', '')
        bib = bt.loads(bib_str)

        entries = bib.entries
        if len(entries) > 1:
            entries = [e for e in entries
                if e['ENTRYTYPE'] in BibtexMetadata._PUB_TYPES]
            assert len(entries) == 1

        data = entries[0]
        return cls.from_dict(data)


    def __init__(self, title, author, year,
            abstract=None, doi=None, url=None, source=None):
        self._title = title
        self._author = author
        self._year = year
        self._abstract = abstract
        self._doi = doi
        self._url = url
        self._source = source


    @property
    def title(self):
        if self._title is None:
            return None
        return self._title.lower().replace('\n', ' ')


    @property
    def authors(self):
        return _parse_bibtex_authors(self._author.lower())


    @property
    def year(self):
        return None if self._year is None else int(self._year)


    @property
    def abstract(self):
        if self._abstract is None:
            return None
        return self._abstract.lower().replace('\n', ' ')


    @property
    def uid(self):
        return super().uid if self._doi is None else ('doi:' + self._doi)


    @property
    def url(self):
        return self._url


    @property
    def source(self):
        return self._source
