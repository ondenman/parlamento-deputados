#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import sha1
import os
import urllib


def hash(str):
    hash = sha1()
    hash.update(str)
    return hash.hexdigest()


def file_get_contents(file):
    return open(file).read()


def file_put_contents(file, contents):
    open(file, 'w+').write(contents)


def getpage(url):
    if not os.path.exists('cache'):
        print 'Creating new cache/ folder.'
        os.mkdir('cache')
    url_hash = hash(url)
    cache_file = 'cache/' + url_hash

    if os.path.exists(cache_file):
        page = file_get_contents(cache_file)
    else:
        page = urllib.urlopen(url).read()
        file_put_contents(cache_file, page)
    return page


def load_csv(filename, keys=[], delimiter=",", quotechar='"', header=False):
    """Parses the content of a CSV file and returns a list of lists,
    or a list of dicts if the key names are indicated in the arguments."""
    import csv
    rows = csv.reader(open(filename), delimiter=delimiter, quotechar=quotechar)
    data = []
    first = True
    for row in rows:
        if first and header:
            first = False
            continue
        row_data = {}
        if keys and len(row) != len(keys):
            print row
            raise IndexError("Key list length (%d) does not match row length (%d)" % (len(keys), len(row)))
        elif keys:
            for key in keys:
                i = keys.index(key)
                row_data[key] = row[i]
            data.append(row_data)
        else:
            data.append(row)
    return data


def replace_letters(s, letters, l):
    '''Replace all specified characters with a substring.'''
    for letter in letters:
        s = s.replace(letter, l)
    return s


def slugify(s):
    '''Creates accent-aware slugs based on human formatted strings.'''
    s = s.strip()
    s = s.lower()
    s = s.replace("-", "")
    s = s.replace(" ", "-")
    s = s.replace("'", "-")
    s = replace_letters(s, u"áàâã", u"a")
    s = replace_letters(s, u"éèê", u"e")
    s = replace_letters(s, u"íì", u"i")
    s = replace_letters(s, u"óòôõ", u"o")
    s = replace_letters(s, u"úù", u"u")
    s = replace_letters(s, u"ç", u"c")
    return s
