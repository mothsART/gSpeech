#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

import os

def replace(text, dict_path):
    print('before', dict_path)
    if not os.path.exists(dict_path):
        return text
    print('after', dict_path)
    with open(dict_path, 'r') as f:
        for line in f.readlines():
            bad = line.split('=')[0]
            if line.find('=') == -1:
                continue
            good = line.split('=')[1].replace('\n', '')
            text = text.replace(bad, good)
    return text

def adaptTextToDict(text, dict_path, lang):
    text = text.replace('\"', '')
    text = text.replace('`', '')
    text = text.replace('´', '')
    if lang != 'fr-FR':
        text = text.replace('-','')
    text = replace(text, dict_path)
    return text

