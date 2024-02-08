import os
from influxdb_client import InfluxDBClient

token = "maxlogadmintoken"
org = "maxlogorg"
bucket = "maxlogbucket"

client = InfluxDBClient(url="http://localhost:8086", token=token)



import csv
import time
from influxdb_client.client.query_api import QueryApi

query_api = client.query_api()
query = f'from(bucket: "{bucket}") |> range(start: -1d)'  # Adjust the range as needed
csv_result = query_api.query_csv(query=query, org=org)

with open(f'measurement_{int(time.time())}.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for row in csv_result:
        writer.writerow(row)



from influxdb_client.client.delete_api import DeleteApi
from datetime import datetime, timezone, timedelta

delete_api = client.delete_api()
stop = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
start = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
delete_api.delete(start, stop, predicate="", bucket=bucket, org=org)

client.close()

