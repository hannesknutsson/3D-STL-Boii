FROM python:3.9.0a6-buster

RUN apt -y update && apt -y upgrade

ADD py/3D-STL-Boii.py .
ADD py/StlToGif.py .
ADD py/3D-STL-Boii.py .
ADD docker/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "3D-STL-Boii.py"]