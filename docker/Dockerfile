FROM python:3 AS buildingstage

RUN python -3 -m pip install -U discord.py
RUN pip install Matplotlib Numpy Numpy-stl imageio

RUN git clone https://github.com/hannesknutsson/3D-STL-Boii.git

ENTRYPOINT ["python", "3D-STL-Boii.py"]