import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import os

# Define your bucket, organization, and token
bucket = "<my-bucket>"
org = "<my-org>"
token = "<my-token>"
url = "http://localhost:8086"  # Adjust the URL if your InfluxDB instance is not running on localhost

# Instantiate the client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Get the write API
write_api = client.write_api(write_options=SYNCHRONOUS)

# Assuming you have a function to read the temperature sensor
def read_temperature():
    # Implement logic here to read from your temperature sensor
    # For example, let's say the temperature is  25.3 degrees Celsius
    return  25.3

# Read the temperature
temp = read_temperature()

# Create a point with the current timestamp and temperature
p = influxdb_client.Point("temperature").field("value", temp).time(influxdb_client.current_utc_time())

# Write the point to InfluxDB
write_api.write(bucket=bucket, org=org, record=p)

# Close the client
client.close()

