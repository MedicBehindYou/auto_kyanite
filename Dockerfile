# syntax=docker/dockerfile:1

# TODO: Build from scratch instead of using a previous image.

FROM 192.168.0.105:8090/kyanite

RUN apt-get update -y && apt-get install python3-pip -y

RUN pip install -U pip

RUN pip install -U numpy scipy matplotlib pandas seaborn 

WORKDIR /app

COPY . /app

ENTRYPOINT ["python3", "-u", "/app/kyanite_db.py"]