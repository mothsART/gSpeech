import codecs
import glob
import os
import re


from .workers.fr_FR import acronyme, roman_numerals


def _replace_txt(text, line):
    bad = line.split('=')[0]
    if line.find('=') == -1:
        return text
    good = line.split('=')[1].replace('\n', '')
    text = text.replace(bad, good)
    return text.replace(bad.capitalize(), good)


def _replace_acronym(text, line):
    bad = line.split('=')[0]
    if line.find('=') == -1:
        return text
    good = line.split('=')[1].replace('\n', '')
    if text.startswith(bad) and text.endswith(bad):
        text = text.replace(bad, good)
    if text.startswith(bad):
        text = text.replace('%s ' % bad, '%s ' % good)
    text = text.replace(' %s' % bad, ' %s' % good)
    text = text.replace(bad.upper(), good)
    return text.replace(bad.capitalize(), good)


def _replace_ponctuation(text, line):
    bad = line.split('=')[0]
    if line.find('=') == -1:
        return text
    good = line.split('=')[1].replace('\n', '')

    text = text.replace(
        """l'%s """ % bad,
        """l'%s """ % good,
    )
    text = text.replace(
        """d'%s """ % bad,
        """d'%s """ % good,
    )
    text = text.replace(
        """L'%s """ % bad,
        """l'%s """ % good,
    )
    text = text.replace(
        """D'%s """ % bad,
        """d'%s """ % good,
    )
    text = text.replace(bad + '.', good + '.')
    text = text.replace(bad + ';', good + ';')
    text = text.replace(bad + ',', good + ',')
    text = text.replace(bad + '?', good + '?')
    text = text.replace(bad + '!', good + '!')
    text = re.sub(bad + '$', good, text)

    if text.startswith(bad):
        text = text.replace(bad + ' ', good + ' ')
    if text.find(' %s' % bad) != -1:
        text = text.replace(bad + ' ', good + ' ')
    text = re.sub(bad + ' $', good, text)
    return text


def replace(text, dict_path):
    if not os.path.isdir(dict_path):
        return text
    dict_list = glob.glob('%s/*dic' % dict_path)
    for path in sorted(dict_list):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                text = _replace_txt(text, line)

    dict_acronym_list = glob.glob('%s/*dic.acronym' % dict_path)
    for path in sorted(dict_acronym_list):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                text = _replace_acronym(text, line)

    dict_ponctuation_list = glob.glob('%s/*dic.ponctuation' % dict_path)
    for path in sorted(dict_ponctuation_list):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                text = _replace_ponctuation(text, line)
    return text


def text_to_dict(text, dict_path, lang, debug=False):
    if debug:
        print('before :', text)
    # remove multiple spaces in a string
    text = ' '.join(text.split())
    # remove quotes
    text = text.replace('\"', '')
    text = text.replace('`', '')
    text = text.replace('´', '')

    text = replace(text, dict_path)
    if lang == 'fr-FR':
        text = roman_numerals.replace(text)
        text = acronyme.too_consonnant(text)
    if debug:
        print('after :', text.lower())
    return text.lower()
