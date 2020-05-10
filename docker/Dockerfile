FROM python:3.9.0a6-buster

RUN apt -y update && apt -y upgrade
RUN apt -y install git

RUN pip install --upgrade pip

RUN pip install requirements.txt

#RUN python -m pip install -U discord.py

ADD py/*

ENTRYPOINT ["python", "3D-STL-Boii.py"]