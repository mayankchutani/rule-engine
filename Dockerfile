#
# Copyright 2016 Woocation Technologies
#

FROM woocation/anaconda3
MAINTAINER Woocation

RUN apt-get update

ADD . /insight
WORKDIR /insight

RUN conda install --yes --file conda_requirements.txt
RUN pip install -r pip_requirements.txt

ENV MONGO_URI ''

EXPOSE 5000
CMD ["python", "driver.py"]