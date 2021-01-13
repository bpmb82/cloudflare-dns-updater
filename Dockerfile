# Build a virtualenv using the appropriate Debian release
# * Install python3-venv for the built-in Python3 venv module (not installed by default)
# * Install gcc libpython3-dev to compile C Python modules
# * Update pip to support bdist_wheel
FROM debian:buster-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Stage 3, copy the venv and scripts into a distroless image

FROM gcr.io/distroless/python3-debian10

ENV HEALTHFILE "/healthcheck"

COPY --from=build-venv /venv /venv
WORKDIR /app
COPY healthcheck.py .
COPY cloudflare-dns-updater.py .

HEALTHCHECK --interval=2m --timeout=5s \
  CMD [ "/venv/bin/python3", "-u", "healthcheck.py" ]

ENTRYPOINT ["/venv/bin/python3", "-u", "cloudflare-dns-updater.py"]
