# syntax=docker/dockerfile:1

# TODO: Build from scratch instead of using a previous image.

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

RUN pip install -U pip --break-system-packages

RUN pip install -U numpy scipy matplotlib pandas seaborn --break-system-packages

RUN pip install -U configparser --break-system-packages

COPY . /app

ENTRYPOINT ["python3", "-u", "/app/main.py"]