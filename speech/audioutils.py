import multiprocessing
import os
import subprocess

from .i18n import _text_to_long


def effect(text, speed=100, pitch=100, volume=120):
    _speed = '<speed level="%s">%s</speed>' % (speed, text)
    _pitch = '<pitch level="%s">%s</pitch>' % (pitch, _speed)
    return '<volume level="%s">%s</volume>' % (volume, _pitch)


def get_audio_commands(text, outfile, lang, cache_path, speed):
    overflow_len = 30000
    cmds = []
    names = []
    # remove parenthesis to avoid bugs with pico2wave command
    text = text.replace('"', '')
    text = text.replace("'", '')
    # low the limits to avoid overflow
    if len(text) <= overflow_len:
        cmds.append(['pico2wave', '-l', lang, '-w', outfile, '--',
                     effect(text, speed * 100)])
        names.append(outfile)
        return names, cmds
    discours = text.split('.')
    text = ''
    for idx, paragraph in enumerate(discours):
        text += paragraph
        if (
            idx == len(discours) - 1
            # low the limits to avoid overflow
            or len(text) + len(discours[idx + 1]) >= overflow_len
        ):
            filename = cache_path + '/speech' + str(idx) + '.wav'
            cmds.append(
                ['pico2wave', '-l', lang, '-w', filename, '--',
                 effect(text, speed * 100)]
            )
            names.append(filename)
            text = ''
    return names, cmds


def shell(cmd):
    return subprocess.call(cmd)


def run_audio_files(names, cmds, outfile='out.wav'):
    if len(cmds) == 1:
        subprocess.Popen(cmds[0]).communicate()
        return
    p = subprocess.Popen(
        ['which', 'sox'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    path, _ = p.communicate()
    # rstrip is used to remove trailing spaces, that cause isfile function to
    # fail even if sox is present
    if not os.path.isfile(path.rstrip()):
        return
    nproc = int(.5 * multiprocessing.cpu_count())
    if nproc == 0:
        nproc = 1
    multiprocessing.Pool(nproc).map(shell, cmds)

    subprocess.Popen(['sox'] + names + [outfile]).communicate()

    for _file in names:
        os.remove(_file)
