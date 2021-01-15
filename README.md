# cloudflare-dns-updater

A simple docker image that can update your Cloudflare DNS if you have a Dynamic IP

# Installation

Use the included docker-compose.yml and update it with your own hostname and Cloudflare token.

To create a token, see: https://developers.cloudflare.com/api/tokens/create

## Environment variables

* HOST: your hostname (e.g. example.com) or comma-separated list of hostnames (e.g. first.example.com,second.example.com)
* TOKEN: your Cloudflare token
* TIMEOUT: timeout in seconds between checks (default 60 seconds)

## Docker-compose
```
version: '3'

services:

  python-container:
    image: bpmbee/cloudflare-dns-updater:latest # or :distroless
    environment:
      - HOST=example.com,another.example.com
      - TOKEN=YOURCLOUDFLARETOKEN
      - TIMEOUT=60
    restart: unless-stopped```
