#!/bin/sh

FILE_AGE=$((x=$TIMEOUT*3,z=x/$TIMEOUT))

HEALTH=$(find $HEALTHFILE -mtime +$FILE_AGE)

[[ ! -z "$HEALTH" ]] && exit 1 || exit 0
