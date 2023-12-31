# syntax=docker/dockerfile:1

FROM rust:latest as builder

WORKDIR /app

RUN cargo install kyanite

FROM debian:latest

RUN apt-get update && apt-get install -y \
    ca-certificates \
    python3-pip \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
	
COPY --from=builder /usr/local/cargo/bin/kyanite /app/kyanite

WORKDIR /app

RUN pip install -U pip numpy scipy matplotlib pandas seaborn configparser --break-system-packages

COPY . /app

RUN mkdir /config && mv config.ini /config/config.ini && mv entries.txt /config/entries.txt

RUN chmod 777 * && cd /config && chmod 777 *

ENTRYPOINT ["python3", "-u", "/app/main.py"]