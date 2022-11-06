import getopt
import os
import sys
from os.path import basename, dirname, isdir, isfile, join

from . import __version__
from .api import Player
from .utils import concat_list


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
            '             file to read (supported only plain text)\n'
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
    def read():
        return CliOption(
            '-r', '--read',
            '                   read text\n'
        )

    @staticmethod
    def debug():
        return CliOption(
            '-d', '--debug',
            '                  debug mode\n'
        )


def cli_help(conf):
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
        str(CliOptions.read()),
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
    return ''.join(value) + concat_list(conf.list_voice_speed)


def read_input_file(file_name):
    """Read input file"""
    if not isfile(file_name):
        print('Error: file not found')
        exit(os.EX_IOERR)
    with open(file_name, 'r') as f:
        return f.read()


def get_output_file(outfile):
    _filename = basename(outfile)
    if not _filename.endswith('.wav'):
        print(
            """Error: the audio output file hasn't a .wav extension"""
        )
        exit(os.EX_DATAERR)
    if _filename == outfile:
        return join(os.getcwd(), outfile)
    _dirname = dirname(outfile)
    if isdir(_dirname):
        return outfile
    try:
        os.makedirs(_dirname, exist_ok=True)
    except Exception:
        print(
            """Error: can't create %s directory' % _dirname"""
        )
    return outfile


def main():
    read = False
    input_file = text = lang = ''
    speed = 1
    outfile = join(os.getcwd(), 'speech.wav')
    player = Player()
    conf = player.conf
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'hvi:f:l:s:o:r:d',
            [
                'help',
                'version',
                'input-text=',
                'input-file=',
                'lang=',
                'speed=',
                'output-file=',
                'read=',
                'debug='
            ]
        )
    except getopt.GetoptError:
        print(cli_help(conf))
        exit(os.EX_USAGE)
    if len(opts) == 0:
        print(cli_help(conf))
        exit(os.EX_OK)
    for opt, arg in opts:
        if opt in CliOptions.help_view():
            print(cli_help(conf))
            exit(os.EX_OK)
        if opt in CliOptions.version():
            print('%s version %s' % (conf.app_name, __version__))
            exit(os.EX_OK)
        if opt in CliOptions.read():
            read = True
        if opt in CliOptions.debug():
            player.debug = True
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
        player.set_lang(lang)
    if speed in conf.list_voice_speed:
        player.set_speed(speed)
    else:
        speed = conf.voice_speed
    if input_file:
        text = read_input_file(input_file)
    conf.temp_path = get_output_file(outfile)

    if read:
        player.read(text, lang, speed)
        return
    player.convert(text, lang, speed)
