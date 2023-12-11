FROM node:21

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt
COPY ./app /src/app
COPY .solhint.json /src/.solhint.json
COPY ./contracts /src/contracts

ENV PIP_ROOT_USER_ACTION=ignore


RUN apt-get update && apt-get -y dist-upgrade;
RUN apt-get update && apt-get install -y
RUN apt-get install -y python3.11  python3-pip python3-launchpadlib gdebi graphviz

# Python 3.7 installation - required for Securify
RUN apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev -y
RUN wget https://www.python.org/ftp/python/3.7.16/Python-3.7.16.tar.xz
RUN tar -xf Python-3.7.16.tar.xz
RUN cd Python-3.7.16  && \
        ./configure --enable-optimizations --enable-shared && \
        make -j8 build_all  && \
        make -j8 altinstall  && \
        ldconfig /usr/local/share/python3.7



# Solhint
RUN npm install -g solhint

# Slither
# https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3
ENV PIP_BREAK_SYSTEM_PACKAGES 1 

RUN pip3 install slither-analyzer

# Smartcheck
RUN npm install -g @smartdec/smartcheck 
RUN smartcheck -p contracts/testContract.sol # first usage install jre

# Securify
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:ethereum/ethereum -y
RUN apt update -y

RUN wget http://ftp.de.debian.org/debian/pool/main/libf/libffi/libffi6_3.2.1-9_amd64.deb \
        -O /tmp/libffi6.deb && \
        dpkg -i /tmp/libffi6.deb
RUN wget https://github.com/souffle-lang/souffle/releases/download/1.6.2/souffle_1.6.2-1_amd64.deb \
        -O /tmp/souffle.deb && \
        gdebi --n /tmp/souffle.deb
RUN apt update -y


RUN git clone https://github.com/eth-sri/securify2.git
RUN cd securify2 &&  python3.7 setup.py install && \
        python3.7 -m pip install -r requirements.txt && \
        python3.7 -m pip install requests


RUN cd securify2/securify/staticanalysis/libfunctors/ && ./compile_functors.sh
RUN cd securify2/securify/staticanalysis/souffle_analysis && \
                souffle --dl-program=../dl-program \
                --fact-dir=/src/securify2/securify/staticanalysis/facts_in \
                --output-dir=/src/securify2/securify/staticanalysis/facts_out \
                -L../libfunctors -w analysis.dl



ENV LD_LIBRARY_PATH /src/securify2/securify/staticanalysis/libfunctors

RUN solc-select install 0.5.2  && \
        solc-select install latest && \
        solc-select use 0.5.2


RUN  pip install -r /src/requirements.txt











