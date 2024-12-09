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

export_file_name = f'measurement_{int(time.time())}.csv'
with open(export_file_name, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for row in csv_result:
        writer.writerow(row)



def is_file_empty(file_path):
    if os.path.exists(file_path):
        return os.path.getsize(file_path) == 0
    else:
        raise FileNotFoundError("File not found")

try:
    if is_file_empty(export_file_name):
        print("The exported file is empty and will be deleted.")
        os.remove(export_file_name)
except FileNotFoundError as fnf:
    print(fnf)



from influxdb_client.client.delete_api import DeleteApi
from datetime import datetime, timezone, timedelta

delete_api = client.delete_api()
stop = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
start = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
delete_api.delete(start, stop, predicate="", bucket=bucket, org=org)

client.close()

