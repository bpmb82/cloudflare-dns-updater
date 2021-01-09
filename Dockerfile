FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY healthcheck.sh ./
COPY cloudflare-dns-updater.py ./

HEALTHCHECK --interval=2m --timeout=5s \ 
  CMD ./healthcheck.sh

CMD [ "python", "./cloudflare-dns-updater.py" ]
