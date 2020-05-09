FROM python:3.9.0a6-alpine3.11

RUN apk update && apk upgrade
RUN apk add git 

#RUN python -m pip install -U discord.py

RUN echo ""
RUN echo "mat"

RUN pip install Matplotlib Numpy Numpy-stl imageio discord.py

RUN echo ""
RUN echo "nump"

RUN pip install Matplotlib Numpy Numpy-stl imageio discord.py

RUN echo ""
RUN echo "stl"

RUN pip install Matplotlib Numpy Numpy-stl imageio discord.py

RUN echo ""
RUN echo "ima"

RUN pip install Matplotlib Numpy Numpy-stl imageio discord.py

RUN echo ""
RUN echo "disc"

RUN pip install Matplotlib Numpy Numpy-stl imageio discord.py


RUN git clone https://github.com/hannesknutsson/3D-STL-Boii.git

WORKDIR /3D-STL-Boii
ENTRYPOINT ["python", "3D-STL-Boii.py"]