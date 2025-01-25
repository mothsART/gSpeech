.PHONY: unittest flake8 test docker.build.test docker.run.test docker.build.ubuntu-18.04 docker.run.ubuntu-18.04 docker.build.ubuntu-20.04 docker.run.ubuntu-20.04 build.debian deploy.debian clean

mo:
	./compile_language.sh

unittest:
	python3 -m unittest

flake8:
	flake8 --filename="*.py,./gspeech,./gspeech-cli"

test:
	make unittest
	make flake8

docker.build.test:
	docker build -t gspeech/test docker/tests

docker.run.test:
	docker run -i -t gspeech/test /bin/bash

docker.build.ubuntu-18.04:
	docker build -t gspeech/ubuntu-18.04 docker/ubuntu-18.04

docker.run.ubuntu-18.04:
	docker run -i -t gspeech/ubuntu-18.04 /bin/bash

docker.build.ubuntu-20.04:
	docker build -t gspeech/ubuntu-20.04 docker/ubuntu-20.04

docker.run.ubuntu-20.04:
	docker run -i -t gspeech/ubuntu-20.04 /bin/bash

build.debian:
	debuild -us -uc #binary package : .deb, alias of dpkg-buildpackage -rfakeroot -d -us -uc

build.debian.source:
	debuild -S #source package : alias of dpkg-buildpackage -rfakeroot -d -us -uc -S

build.nix:
	nix build

deploy.debian:
	debuild -S
	dput ppa:jerem-ferry/tts `/bin/ls -d ../gspeech*.changes`

clean:
	rm -f MANIFEST
	rm -rf build dist
	git clean -xdf # dry run : git clean -xdn
