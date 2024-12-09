###
# To collect voltage measurements from the owon oscilloscope
###
# Requires:
# vds1022
###

from vds1022 import *
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from datetime import datetime, timezone

# Define your bucket, organization, and token
bucket = "maxlogbucket"
org = "maxlogorg"
token = "maxlogadmintoken"
url = "http://localhost:8086"  # Adjust the URL if your InfluxDB instance is not running on localhost

# Instantiate the client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Get the write API
write_api = client.write_api(write_options=SYNCHRONOUS)

dev = VDS1022(debug=0)
dev.set_channel(CH1, range='100v', offset=1/100, probe='x100')
dev.set_channel(CH2, range='100v', offset=1/100, probe='x100')

for frames in dev.fetch_iter(freq=10):
    now = int(datetime.now(timezone.utc).timestamp() * 1e9)
    p1 = influxdb_client.Point("voltages").field("ch1", frames.ch1.rms()).time(now)
    p2 = influxdb_client.Point("voltages").field("ch2", frames.ch2.rms()).time(now)
    write_api.write(bucket=bucket, org=org, record=p1)
    write_api.write(bucket=bucket, org=org, record=p2)
    print(f"Vrms: {frames.ch1.rms()}", end='\r')

# Close the client
client.close()
