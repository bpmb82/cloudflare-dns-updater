import pathlib
import os
import time

# Assign the environment variables
healthcheck_file = os.getenv('HEALTHFILE')
timeout = int(os.getenv('TIMEOUT'))*3

# Get the healthcheck_file modification date, check if it exists and get the age of the file
fname = pathlib.Path(healthcheck_file)
assert fname.exists(), f'[ health error ] No such file: {fname}' 
mod = int(fname.stat().st_mtime)
now = int(time.time())
age = now - mod


# exit(1) if age of the file is higher than 3 times the timeout, else exit(0)
if age > timeout:
    exit(1)
else:
    exit(0)
