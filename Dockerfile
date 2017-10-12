FROM continuumio/anaconda3:4.4.0
MAINTAINER Mayank Chutani

RUN apt-get update

ADD . /insight
WORKDIR /insight

RUN conda install --yes --file conda_requirements.txt
RUN pip install -r pip_requirements.txt

ENV MONGO_URI ''

EXPOSE 5000
CMD ["python", "driver.py"]
