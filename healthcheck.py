import pathlib
import time

# Assign the environment variables
healthcheck_file = os.getenv('HEALTHFILE')
timeout = int(os.getenv('TIMEOUT'))*3

# Get the healthcheck_file modification date, check if it exists and get the age of the file
fname = pathlib.Path(healthcheck_file)
ts = time.ctime(time.time())
assert fname.exists(), f'{ts} [ health error ] No such file: {fname}' 
mod = int(fname.stat().st_mtime)
now = int(time.time())
age = now - mod


# exit(1) if age of the file is higher than 3 times the timeout, else exit(0)
if age > timeout:
    print(time.ctime(time.time()),'[ health error ] Healthcheck failed'
	  exit(1)
else:
    print(time.ctime(time.time()),f'[ health info ] Age of the healthfile was {age}')
    exit(0)
