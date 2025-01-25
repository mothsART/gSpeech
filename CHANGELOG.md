# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased : 1.0]

https://github.com/coqui-ai/TTS
https://github.com/myshell-ai/OpenVoice
https://github.com/daniilrobnikov/vits2

### Added
- GTK unit tests
- support of the two hundred most popular french lastname https://fr.wikipedia.org/wiki/Liste_des_noms_de_famille_les_plus_courants_en_France
- support most popular history names : https://www.histoire-pour-tous.fr/biographies.html

## [0.13.0]
    - bugfix on last Python 3.12 : SafeConfigParser must be replace by ConfigParser
    - some corrections on debian archiv creation

## [0.12.0]
    - feature : create API : other python project can use gSpeech like a lib
    - feature : read text on cli mode
    - bugfix : correction on cache path
    - bugfix : some corrections on french terms, words, abreviation etc.

## [0.11.0]

### Added
- read roman numerals
- support of the thousand most popular French male firstname : https://motperdu.fr/top-1000-des-prenoms-de-garcons
- support of the thousand most popular French female firstname : https://motperdu.fr/top-1000-des-prenoms-de-filles

## [0.10.1]

### Bugfix

- option doesn't write new conf file.

## [0.10]

### Bugfix

- better sox integration : trigger when text to reach is too long.
- setup.py whith new dict tree
- edit speed on tray change speed on multimedia popup and vice versa
- edit lang on tray change lang on multimedia popup and vice versa

### Added

- speed management : voice speech integration on cli, tray and multimedia menu
- integrate sox into nix
- screenshots

## [0.9.2]

### Bugfix

- create all directories on a pid new path

## [0.9.1]

### Bugfix

- test permissions before write a conf file

## [0.9]

### Bugfix

- french text : 'fan'
- correction on about dialog
- give a parent on all dialogs (gtk warning)

### Added

- option dialog : can enable/disable notification popup
- create a changelog file
- create a Debian package
- create a ppa : https://launchpad.net/~jerem-ferry/+archive/ubuntu/tts
- create a nix build
- flake8 (and travisCI integration)
