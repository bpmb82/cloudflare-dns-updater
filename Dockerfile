# Stage 1, install the requirements in a venv

FROM python:3.9.1-slim-buster AS build-env

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2, copy the venv and scripts into a distroless image

FROM gcr.io/distroless/python3-debian10

ENV HEALTHFILE "/healthcheck"

COPY --from=build-env /venv /venv
WORKDIR /usr/src/app
COPY healthcheck.py ./
COPY cloudflare-dns-updater.py ./

HEALTHCHECK --interval=2m --timeout=5s \ 
  CMD [ "/venv/bin/python3", "healthcheck.py" ]

ENTRYPOINT [ "/venv/bin/python3", "cloudflare-dns-updater.py" ]
