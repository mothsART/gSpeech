import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

from .audioutils import get_audio_commands, run_audio_files
from .conf import Conf
from .textutils import text_to_dict
from .utils import concat_list


def on_message(bus, message, player):
    """error message on playing function"""
    t = message.type
    if t == Gst.MessageType.EOS:
        # file ended, stop
        player.set_state(Gst.State.NULL)
    if t == Gst.MessageType.ERROR:
        # Error ocurred, print and stop
        player.set_state(Gst.State.NULL)
        err, debug = message.parse_error()
        print('Error: %s' % err, debug)


class Player:
    def __init__(self, debug=False, lang=None, speed=1):
        self.conf = Conf()
        self.debug = debug
        if lang:
            self.set_lang(lang)
        if speed != 1:
            self.set_speed(speed)
        Gst.init('')
        self.pipe = Gst.Pipeline()

    def set_ui(self, ui=False):
        if not ui:
            return
        self.pipe = Gst.ElementFactory.make('playbin', 'player')
        self.pipe.set_property('uri', 'file://%s' % self.conf.temp_path)
        bus = self.pipe.get_bus()
        bus.add_signal_watch()
        bus.connect('message', on_message, self.pipe)

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
        self.convert(text, lang=None, speed=1)
        playbin = Gst.ElementFactory.make('playbin', 'player')
        playbin.set_property('uri', 'file://%s' % self.conf.temp_path)
        self.pipe.add(playbin)
        self.play()
        bus = self.pipe.get_bus()
        bus.timed_pop_filtered(
            Gst.CLOCK_TIME_NONE,
            Gst.MessageType.ERROR | Gst.MessageType.EOS
        )
        self.stop()

    def stop(self):
        self.pipe.set_state(Gst.State.NULL)

    def play(self):
        self.pipe.set_state(Gst.State.PLAYING)

    def pause(self):
        self.pipe.set_state(Gst.State.PAUSED)

    def get_state(self):
        return self.pipe.get_state(Gst.CLOCK_TIME_NONE)[1]
