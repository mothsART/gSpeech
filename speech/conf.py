import os
import sys
from configparser import RawConfigParser, ConfigParser
from os.path import dirname, expanduser, isfile, join

import gi

from .debug import is_debug_mode
from .i18n import _comment, _developpers


def ini_read(config_path, section, key, default):
    if isfile(config_path):
        parser = ConfigParser()
        parser.read(config_path)
        try:
            _property = parser.get(section, key)
        except Exception:
            _property = default
    else:
        _property = default
    if _property.lower() in ['1', 'yes', 'true', 'on']:
        return True
    if _property.lower() in ['0', 'no', 'false', 'off']:
        return False
    return _property


class Conf:
    app_name = 'gSpeech'
    # Temporaries files
    cache_path = join(os.getenv('HOME'), '.cache', app_name)

    developers = [
        ['Lahire Biette', '<tuxmouraille@gmail.com>'],
        ['Sardi Carlo', '<lusumdev@zoho.eu>'],
        ['Ferry Jérémie', '<jerem.ferry@gmail.com>']
    ]
    copyright_year = '2011, 2014, 2018, 2020'
    copyrights = 'Copyright © %s %s' % (
        copyright_year,
        ', '.join([name for name, mail in developers])
    )

    # Supported SVOX Pico's languages
    list_langs = ['de-DE', 'en-GB', 'en-US', 'es-ES', 'fr-FR', 'it-IT']

    voice_speed = 1

    list_voice_speed = [0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2]

    translators = [
        'Dupouy Paul (it-IT)',
        'Ferry Jérémie (fr-FR)'
    ]

    website = 'https://github.com/mothsart/gSpeech'

    show_notification = True
    has_app_indicator = True
    lang = ''

    def set_dict(self, lang):
        self.dict_path = join(
            self.share_path,
            'gspeech/dict',
            lang.replace('-', '_')
        )
        if is_debug_mode():
            self.dict_path = join(
                self.dir,
                'dict',
                lang.replace('-', '_')
            )

    def set_lang(self, lang):
        if lang in self.list_langs:
            self.lang = lang
        if self.icons_dir:
            self.icon_path = join(
                self.icons_dir,
                self.app_name + '-' + lang + '.svg'
            )
        self.set_dict(lang)

    def set_speed(self, speed):
        if speed in self.list_voice_speed:
            self.voice_speed = speed

    def __init__(self, script_dir=None):
        self.create_cache()
        self.pid = join(self.cache_path, 'gspeech.pid')
        self.temp_path = join(self.cache_path, 'speech.wav')

        self.dir = join(expanduser('~'), '.config/gSpeech')

        self.share_path = join(
            dirname(sys.modules['speech'].__file__),
            '..', '..', '..', '..', 'share'
        )
        self.local_dir = join(self.share_path, 'locale')
        self.icons_dir = join(
            self.share_path, 'icons/hicolor/scalable/apps'
        )
        if is_debug_mode():
            self.dir = join(dirname(dirname(__file__)))
            self.local_dir = join(self.dir, 'locale')
            self.icons_dir = join(self.dir, 'icons')

        self.path = join(self.dir, 'gspeech.conf')

        self.has_app_indicator = bool(ini_read(
            self.path, 'CONFIGURATION', 'USEAPPINDICATOR', 'True'
        ))

        lang = str(ini_read(
            self.path, 'CONFIGURATION', 'DEFAULTLANGUAGE', ''
        ))

        self.voice_speed = float(ini_read(
            self.path, 'CONFIGURATION', 'VOICESPEED', '1'
        ))

        self.show_notification = bool(ini_read(
            self.path,
            'CONFIGURATION',
            'SHOWNOTIFICATION',
            'True'
        ))
        self.lang = lang[:2] + '-' + lang[3:][:2]
        # if SVOX Pico not support this language, find os environment language
        if self.lang not in self.list_langs:
            self.lang = os.environ.get('LANG', 'en_US')[:2]
            self.lang += '-' + os.environ.get('LANG', 'en_US')[3:][:2]
            # if SVOX Pico not support this language, use US english
            if self.lang not in self.list_langs:
                self.lang = 'en-US'

        try:
            gi.require_version('AppIndicator3', '0.1')
            from gi.repository import AppIndicator3  # noqa: F401
            print('status : appindicator 3')
        except (ValueError, ImportError):
            self.has_app_indicator = False
            print('status : other')

        self.set_lang(self.lang)

        self.comment = _comment
        self.authors = '%s %s' % (
            _developpers,
            ', '.join([
                '%s (%s)' % (name, mail.replace('<', '').replace('>', ''))
                for name, mail in self.developers
            ]),
        )
        self.license = """
        Copyright © {0}
        {1}

        {2} is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        {2} is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with {2}.  If not, see <http://www.gnu.org/licenses/>.
        """.format(
            self.copyright_year,
            self.authors,
            self.app_name
        )

        if not isfile(self.path):
            self.update()

    def create_cache(self):
        if isfile(self.cache_path):
            return
        try:
            os.makedirs(self.cache_path, exist_ok=True)
            return
        except Exception:
            import tempfile
            self.cache_path = tempfile.mkdtemp()

    def update(self):
        raw = RawConfigParser()
        raw.add_section('CONFIGURATION')
        raw.set(
            'CONFIGURATION',
            'USEAPPINDICATOR',
            self.has_app_indicator
        )
        raw.set(
            'CONFIGURATION',
            'DEFAULTLANGUAGE',
            self.lang
        )
        raw.set(
            'CONFIGURATION',
            'VOICESPEED',
            self.voice_speed
        )
        raw.set(
            'CONFIGURATION',
            'SHOWNOTIFICATION',
            self.show_notification
        )
        try:
            os.makedirs(self.dir, exist_ok=True)
            with open(self.path, 'w+') as stream:
                raw.write(stream)
        except Exception:
            return False
        return True
