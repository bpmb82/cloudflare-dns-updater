FROM python:3.9.1-alpine3.12

ENV HEALTHFILE "/healthcheck"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY healthcheck.sh ./
COPY cloudflare-dns-updater.py ./

HEALTHCHECK --interval=2m --timeout=5s \ 
  CMD ./healthcheck.sh

CMD [ "python", "./cloudflare-dns-updater.py" ]
