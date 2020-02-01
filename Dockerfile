FROM ufoym/deepo

RUN apt-get update
RUN apt-get -y install python3-venv python3-dev

RUN pip install --upgrade pip
RUN pip install transformers