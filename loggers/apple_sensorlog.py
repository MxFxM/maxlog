###
# This is to log json data coming from the apple app "SensorLog" via TCP server
###
# Requires:
###

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
import socket
import json
import select
import sys

# Define your bucket, organization, and token
bucket = "maxlogbucket"
org = "maxlogorg"
token = "maxlogadmintoken"
url = "http://localhost:8086"  # Adjust the URL if your InfluxDB instance is not running on localhost

# Instantiate the client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Get the write API
write_api = client.write_api(write_options=SYNCHRONOUS)

# Class to handle TCP connection
class TCPConnection:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.buffer = b''
        self.counter = 0

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            print('Successful Connection')
        except Exception as e:
            print(f'Connection Failed: {e}')

    def readlines(self):
        while True:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.001)
            if rlist:
                key = sys.stdin.read(1)
                if key == 'q':
                    break
            data = self.sock.recv(1024)
            if not data:
                break
            self.buffer += data
            self.parse_json()

    def parse_json(self):
        # Find complete JSON packets in the buffer
        start = 0
        while True:
            end = self.buffer.find(b'}', start)
            if end == -1:
                break
            end += 1  # Include the '}' character
            json_packet = self.buffer[start:end]
            self.buffer = self.buffer[end:]
            try:
                json_data = json.loads(json_packet.decode('utf-8'))
                self.handle_json(json_data)
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                # If decoding fails, move the start pointer forward to try again
                start += 1
                continue
            start = 0

    def handle_json(self, json_data):
        # Handle the parsed JSON data here
        #print(json_data)
        self.counter = self.counter + 1
        print(self.counter)

        # Get the current UTC time in nanoseconds
        now = int(datetime.now(timezone.utc).timestamp() * 1e9)

        # Create a point
        p = influxdb_client.Point("sensorlog")

        # Add fields from json
        for key, value in json_data.items():
            try:
                p.field(key, float(value))
            except ValueError:
                p.field(key, str(value))

        #  Add current timestamp
        p.time(now)

        # Write the point to InfluxDB
        write_api.write(bucket=bucket, org=org, record=p)

# Create TCP client and connect to host
listen = TCPConnection()
listen.connect('192.168.188.53', 59526)

# Read incoming packets until end or q-key and ENTER is pressed
listen.readlines()

# Close the influx client
client.close()

