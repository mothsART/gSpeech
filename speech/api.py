import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

from .audioutils import get_audio_commands, run_audio_files
from .conf import Conf
from .textutils import text_to_dict
from .utils import concat_list
from .widgets.events import on_player


class Player:
    def __init__(self, debug=False, lang=None, speed=1):
        Gst.init('')
        self.conf = Conf()
        self.debug = debug
        if lang:
            self.set_lang(lang)
        if speed != 1:
            self.set_speed(speed)

    def set_lang(self, lang):
        if lang in self.conf.list_langs:
            self.conf.set_lang(lang)
            return

        raise Exception(
            'lang not in this list : %s'
            % concat_list(self.conf.list_langs)
        )

    def set_speed(self, speed):
        if speed not in self.conf.list_voice_speed:
            raise Exception(
                'Speed value must be one of these values : %s'
                % concat_list(self.conf.list_voice_speed)
            )
        self.conf.set_speed(speed)

    def convert(self, text, lang=None, speed=1):
        if lang:
            self.set_lang(lang)
        if speed != 1:
            self.set_speed(speed)
        text = text_to_dict(
            text,
            self.conf.dict_path,
            self.conf.lang,
            self.debug
        )
        names, cmds = get_audio_commands(
            text,
            self.conf.temp_path,
            self.conf.lang,
            self.conf.cache_path,
            self.conf.voice_speed
        )
        run_audio_files(names, cmds, self.conf.temp_path)

    def read(self, text, lang=None, speed=1):
        _player = on_player(self.conf.temp_path)
        self.convert(text, lang=None, speed=1)
        _player.set_state(Gst.State.PLAYING)
