#!/usr/bin/env python3

from selenium import webdriver
from fuzzywuzzy import fuzz
from requests.utils import urlparse
import os

_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
DEF_WEBDRIVER_PATH = '/home/erik/webdriver'
DEF_PAGE_LOAD_TIMEOUT = 25
MAX_N_RETRIES = 3
GOOGLE_URL = 'http://google.com'


def retry(max_n_times=1, verbose=True):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            for i in range(max_n_times):
                try:
                    ret = fn(*args, **kwargs)
                    return ret
                except Exception as e:
                    if verbose:
                        print('FAIL #{} @{}: "{}" - trying again'.format(
                            i+1, fn.__name__, e))
                    exc = e
            else:
                raise exc
        return wrapper
    return decorator


def get_headless_chrome_browser(
        webdriver_path, page_load_timeout=DEF_PAGE_LOAD_TIMEOUT):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(webdriver_path, chrome_options=options)
    if page_load_timeout is not None:
        driver.set_page_load_timeout(page_load_timeout)
    return driver


def get_chrome_browser(webdriver_path, page_load_timeout=DEF_PAGE_LOAD_TIMEOUT):
    driver = webdriver.Chrome(webdriver_path)
    if page_load_timeout is not None:
        driver.set_page_load_timeout(page_load_timeout)
    return driver


def is_in_domain(driver, netloc):
    driver_meta = urlparse(getattr(driver, 'current_url', ''))
    return driver_meta.netloc == netloc


def is_in_page(driver, url):
    meta_a = urlparse(url)
    meta_b = urlparse(getattr(driver, 'current_url', ''))
    return all([
        meta_a.netloc == meta_b.netloc,
        meta_a.path.rstrip('/') == meta_b.path.rstrip('/'),
    ])


@retry(MAX_N_RETRIES)
def access(driver, url, refresh=False):
    if refresh or not is_in_page(driver, url):
        driver.get(url)


def put_text(elem, text, clear=True):
    if clear:
        elem.clear()
    elem.send_keys(text)


def click(elem):
    elem.click()


def get_search_query_url(query):
    return '{}/search?q={}'.format(GOOGLE_URL, query.replace('=', ''))


def get_search_results_list_elem(driver):
    return driver.find_element_by_id('search')


def get_search_result_elems_from_list_elem(elem):
    return elem.find_elements_by_class_name('rc')


def get_header_elem_from_search_result_elem(elem):
    return elem.find_elements_by_class_name('r')[0]


def get_title_elem_from_search_header_elem(elem):
    return elem.find_elements_by_tag_name('h3')[0]


def get_text_elems_from_search_result_elem(elem):
    return elem.find_elements_by_class_name('fl')


def get_title_from_search_result_elem(elem):
    header_elem = get_header_elem_from_search_result_elem(elem)
    title = header_elem.text.split('\n')[0]
    return title


def get_citation_text_from_search_result_text_elems(elems):
    for elem in elems:
        if is_citation_text(elem.text):
            return elem.text
    return None


def is_citation_text(text):
    text = text.lower()
    prefixes = [
        'cited by',
        'citado por',
    ]
    return any(text.startswith(p) for p in prefixes)


def get_citation_number(text):
    number_str = text.split(' ')[-1]
    return int(number_str)


def get_query_match(query, result_title):
    return fuzz.ratio(query.lower(), result_title.lower())/100


class User:
    def __init__(self, driver_or_path, verbose=True):
        self.info = print if verbose else (lambda *a, **ka: None)

        self.driver = driver_or_path
        if isinstance(driver_or_path, str):
            self.info('opening driver...', flush=True, end=' ')
            self.driver = get_chrome_browser(driver_or_path)
            self.info('done')


    def access(self, url, refresh=False):
        self.info('acessing "{}"...'.format(url), flush=True, end=' ')
        access(self.driver, url, refresh=refresh)
        self.info('done.')


    def search(self, query):
        url = get_search_query_url(query)
        self.access(url)


    def get_paper_info(self, query):
        try:
            self.search(query)
        except Exception as e:
            raise Exception('could not perform search: "{}"'.format(e))

        try:
            results_list = get_search_results_list_elem(self.driver)
        except Exception as e:
            raise Exception('could not get results list elem: "{}"'.format(e))

        try:
            results = get_search_result_elems_from_list_elem(results_list)
            result = results[0]
        except Exception as e:
            raise Exception('could not get first search result: "{}"'.format(e))

        try:
            title = get_title_from_search_result_elem(result)
        except Exception as e:
            raise Exception('could not get search result title: "{}"'.format(e))

        query_match = get_query_match(query, title)

        try:
            texts = get_text_elems_from_search_result_elem(result)
            citation_text = \
                get_citation_text_from_search_result_text_elems(texts)
            if citation_text is None:
                n_citations = None
            else:
                n_citations = get_citation_number(citation_text)
        except Exception as e:
            raise Exception('could not get number of citations: "{}"'.format(e))

        return {
            'result_title': title,
            'query_match': query_match,
            'n_citations': n_citations,
        }
