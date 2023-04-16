FROM ubuntu:20.04
RUN apt-get update

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jerem-ferry/tts
RUN apt-get update

RUN apt-get -y install gspeech

CMD gspeech-cli -i "Ceci est un test sous docker." -o test_docker.wav

