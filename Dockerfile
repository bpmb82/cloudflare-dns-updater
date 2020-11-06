FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY cloudflare-dns-updater.py ./

CMD [ "python", "./cloudflare-dns-updater.py" ]
