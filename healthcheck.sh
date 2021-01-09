#!/bin/bash

FILE_AGE=$((x=$TIMEOUT+$TIMEOUT,z=x/$TIMEOUT))

HEALTH=$(find /healthcheck -mtime +$FILE_AGE)

[[ ! -z "$HEALTH" ]] && exit 1 || exit 0
