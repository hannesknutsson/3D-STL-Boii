FROM python:latest-alpine

RUN apk update && apk upgrade

RUN python -3 -m pip install -U discord.py
RUN pip install Matplotlib Numpy Numpy-stl imageio

RUN apk add git 

RUN git clone https://github.com/hannesknutsson/3D-STL-Boii.git

ENTRYPOINT ["python", "3D-STL-Boii.py"]