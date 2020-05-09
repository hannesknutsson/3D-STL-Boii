FROM python:latest-alpine

RUN apk update && apk upgrade
RUN apk add git 

#RUN python -m pip install -U discord.py
RUN pip install Matplotlib Numpy Numpy-stl imageio discord.py


RUN git clone https://github.com/hannesknutsson/3D-STL-Boii.git

ENTRYPOINT ["python", "3D-STL-Boii.py"]