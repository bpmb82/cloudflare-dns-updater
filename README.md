# cloudflare-dns-updater

A simple docker image that can update your Cloudflare DNS if you have a Dynamic IP

# Installation

Use the included docker-compose.yml and update it with your own hostname and Cloudflare token.

To create a token, see: https://developers.cloudflare.com/api/tokens/create

## Environment variables

* HOST: your hostname (e.g. example.com)
* TOKEN: your Cloudflare token
* TIMEOUT: timeout in seconds between checks (default 60 seconds)
