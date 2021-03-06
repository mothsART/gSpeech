import getopt
import os
import sys

from speech import __version__
from speech.audioutils import get_audio_commands, run_audio_files
from speech.conf import Conf
from speech.textutils import text_to_dict

conf = Conf()


class CliOption:
    def __init__(self, short, verbose, description):
        self._list = [short, verbose]
        self.description = description

    def __contains__(self, value):
        return value in self._list

    def __str__(self):
        return ''.join((
            '%s   %s' % (self._list[0], self._list[1]),
            self.description
        ))


class CliOptions:
    @staticmethod
    def help_view():
        return CliOption(
            '-h', '--help',
            '                   show usage information\n'
        )

    @staticmethod
    def version():
        return CliOption(
            '-v', '--version',
            '                show version information\n'
        )

    @staticmethod
    def input_text():
        return CliOption(
            '-i', '--input-text',
            '             text to read\n'
        )

    @staticmethod
    def input_file():
        return CliOption(
            '-f', '--input-file',
            '             file to read (supported only plain txt\n'
        )

    @staticmethod
    def output_file():
        return CliOption(
            '-o', '--output-file',
            '            name of the audio output file (wav type)\n'
        )

    @staticmethod
    def lang():
        return CliOption(
            '-l', '--lang',
            '                   language\n'
        )

    @staticmethod
    def speed():
        return CliOption(
            '-s', '--speed',
            '                   voice speed\n'
        )

    @staticmethod
    def debug():
        return CliOption(
            '-d', '--debug',
            '                  debug mode\n'
        )


def cli_help():
    value = (
        '%s version %s' % (conf.app_name, __version__),
        '\nUsage : %s-cli -i "[text to read]" ' % conf.app_name,
        '( or -f [txt file] ) -o [.wav filename] ... ',
        '-l [optional lang]\n',
        '\nCommon flags:\n',
        str(CliOptions.help_view()),
        str(CliOptions.version()),
        str(CliOptions.input_text()),
        str(CliOptions.input_file()),
        str(CliOptions.output_file()),
        str(CliOptions.debug()),
        str(CliOptions.lang()),
        '\npossible languages :',
    )
    for lang in conf.list_langs:
        value += ('\n%s' % lang,)
    value += (
        '\n\n',
        str(CliOptions.speed()),
        '\npossible speech values :',
    )
    for indice, speed in enumerate(conf.list_voice_speed):
        if indice == 0:
            value += (' %s' % str(speed),)
            continue
        value += (', %s' % str(speed),)
    return ''.join(value)


def text_file(file_name):
    """Read text file"""
    if not os.path.isfile(file_name):
        print('Error: file not found')
        exit()
    with open(file_name, 'r') as f:
        return f.read()


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'hvi:f:l:s:o:d',
            [
                'help',
                'version',
                'input-text=',
                'input-file',
                'lang=',
                'speed=',
                'output-file=',
                'debug='
            ]
        )
    except getopt.GetoptError:
        print(cli_help())
        exit(2)
    input_file = text = lang = ''
    debug = False
    speed = 1
    outfile = 'speech.wav'
    if len(opts) == 0:
        print(cli_help())
        exit()
    for opt, arg in opts:
        if opt in CliOptions.help_view():
            print(cli_help())
            exit()
        if opt in CliOptions.version():
            print('%s version %s' % (conf.app_name, __version__))
            exit()
        if opt in CliOptions.debug():
            debug = True
        if opt in CliOptions.lang():
            lang = arg
        elif opt in CliOptions.speed():
            speed = float(arg)
        elif opt in CliOptions.output_file():
            outfile = arg
        elif opt in CliOptions.input_file():
            input_file = arg
        elif opt in CliOptions.input_text():
            text = arg
    if lang in conf.list_langs:
        conf.set_lang(lang)
    if speed in conf.list_voice_speed:
        conf.set_speed(speed)
    else:
        speed = conf.voice_speed
    if input_file:
        text = text_file(input_file)
    text = text_to_dict(text, conf.dict_path, conf.lang, debug)
    names, cmds = get_audio_commands(
        text,
        outfile,
        conf.lang,
        conf.cache_path,
        speed
    )
    run_audio_files(names, cmds, outfile)
