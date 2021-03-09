import os
import subprocess
import sys

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gst, Gtk

from . import notify
from .. import pid
from ..audioutils import get_audio_commands, run_audio_files
from ..i18n import _pause, _play, _read_selected
from ..textutils import text_to_dict


def on_lang(ind, tray, lang, conf):
    """Action on language submenu items"""
    conf.set_lang(lang)
    conf.lang = lang
    conf.update()
    if conf.has_app_indicator:
        ind.set_icon(conf.icon_path)
        return
    tray.set_from_file(conf.icon_path)


def on_speed(speed, conf):
    """Action on voice speed submenu items"""
    conf.set_speed(float(speed))
    conf.voice_speed = float(speed)
    conf.update()


def on_reload(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """Reload GUI"""
    myscript = os.path.abspath(sys.argv[0])
    subprocess.Popen(myscript)
    exit(os.EX_OK)


def on_media_dialog(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """Show multimedia control dialog"""
    if window.get_property('visible'):
        window.hide()
        return
    window.show_all()


def on_destroy(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """Destroy app on clicking Quit item"""
    if os.path.isfile(conf.temp_path):
        os.remove(conf.temp_path)
    pid.remove(conf.pid)
    Gtk.main_quit()


def changed_lang_menu(
    widget, ind, tray, lang, conf, lang_combobox, index=None
):
    on_lang(ind, tray, lang, conf)
    lang_combobox.active = index
    if widget.get_active():
        lang_combobox.set_active(index)


def changed_cb(lang_combobox, ind, tray, conf, menu_langs):
    model = lang_combobox.get_model()
    index = lang_combobox.get_active()
    if index is not None:
        on_lang(ind, tray, model[index][0], conf)
        menu_langs.get_children()[index].set_active(True)


def changed_speed_menu(
    widget, speed, conf, speed_combobox, index=None
):
    on_speed(speed, conf)
    speed_combobox.active = index
    if widget.get_active():
        speed_combobox.set_active(index)


def changed_speed(speed_combobox, conf, menu_voice_speed):
    model = speed_combobox.get_model()
    index = speed_combobox.get_active()
    if index is not None:
        on_speed(model[index][0], conf)
        menu_voice_speed.get_children()[index].set_active(True)


def on_left_click(
    widget,
    conf,
    menu_play_pause,
    win_play_pause,
    player
):
    """
    left click on status icon function
    function like this and not merge with on_execute
    to have possibility to use for something different
    """
    on_execute(widget, None, conf, menu_play_pause, win_play_pause, player)


def on_execute(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """ execute text to speech"""
    if (
        hasattr(widget, 'get_label')
        and widget.get_label() == _read_selected
    ):
        text = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY).wait_for_text()
    else:
        text = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_text()
    notify.get(conf, text)
    if text is None:
        return
    conf.set_lang(conf.lang)

    text = text_to_dict(text, conf.dict_path, conf.lang)
    names, cmds = get_audio_commands(
        text,
        conf.temp_path,
        conf.lang,
        conf.cache_path,
        conf.voice_speed
    )
    run_audio_files(names, cmds, conf.temp_path)
    if player:
        player.stop()
    player.play()
    button_state(menu_play_pause, win_play_pause, player)


def on_play_pause(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """play, pause and stop function for respectives items"""
    if (
        widget.get_label() == Gtk.STOCK_MEDIA_PLAY
        or (
            hasattr(widget, 'get_active')
            and not widget.get_active()
        )
    ):
        player.play()
    else:
        player.pause()
    button_state(menu_play_pause, win_play_pause, player)


def on_stop(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    player.stop()
    button_state(menu_play_pause, win_play_pause, player)


def button_state(menu_play_pause, win_play_pause, player):
    gst_state = player.get_state()
    if gst_state == Gst.State.PLAYING:
        win_play_pause.set_label(Gtk.STOCK_MEDIA_PAUSE)
        menu_play_pause.set_label(_pause)
        menu_play_pause.set_active(False)
        return
    win_play_pause.set_label(Gtk.STOCK_MEDIA_PLAY)
    menu_play_pause.set_label(_play)
    menu_play_pause.set_active(True)
