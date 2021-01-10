FROM python:3.9.1-slim-buster AS build-env

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian10
COPY --from=build-env /venv /venv
WORKDIR /usr/src/app
#COPY healthcheck.sh ./
COPY cloudflare-dns-updater.py ./
#RUN chmod +x ./healthcheck.sh

#HEALTHCHECK --interval=2m --timeout=5s \ 
#  CMD ./healthcheck.sh

ENTRYPOINT [ "/venv/bin/python3", "cloudflare-dns-updater.py" ]
