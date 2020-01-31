FROM nvcr.io/nvidia/tensorflow:18.08-py3

RUN apt-get update
RUN apt-get -y install python3-venv python3-dev

ENV VIRTUAL_ENV=/opt/venv
RUN python3.5 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip uninstall -y tensorflow
RUN pip install tensorflow==1.15

RUN pip uninstall -y pytorch-transformers
RUN pip install transformers==2.3.0