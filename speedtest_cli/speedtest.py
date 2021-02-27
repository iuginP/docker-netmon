import re
import subprocess
import sys, getopt
from influxdb import InfluxDBClient
import time

def speedtest():
    # Execute speedtest on shell
    response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

    # Regex extraction
    ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
    download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
    upload =  re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)

    ping = ping.group(1)
    download = download.group(1)
    upload = upload.group(1)
    return ping, download, upload

def upload_to_db(client, download, upload, ping):
    # Write data to influxdb
    speed_data = [
        {
            "measurement" : "internet_speed",
            "tags" : {
                "host": "RaspberryPiMyLifeUp"
            },
            "fields" : {
                "download": float(download),
                "upload": float(upload),
                "ping": float(ping)
            }
        }
    ]
    return client.write_points(speed_data)


def main(argv):
    # Read arguments
    try:
        opts, args = getopt.getopt(argv,"hu:p:h:di",["user=","password=","host=","database=","port=","interval="])
    except getopt.GetoptError:
        print('speedtest.py -i [--interval=] <minutes> -u [--user=] <user> -p [--password=] <password> -h [--host=] <host>')
        sys.exit(2)
    
    user = None
    password = None
    host = None
    port = '8086'
    database = 'internetspeed'
    time_interval = '30'
    for opt, arg in opts:
        if opt == '-h':
            print('speedtest.py -i [--interval=] <minutes> -u [--user=] <user> -p [--password=] <password> -h [--host=] <host>')
            sys.exit()
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-d", "--database"):
            database = arg
        elif opt in ("--port"):
            port = arg
        elif opt in ("-i", "--interval"):
            time_interval = arg
    time_interval = int(time_interval)

    if user is None or password is None or host is None:
        print('speedtest.py -i [--interval=] <minutes> -u [--user=] <user> -p [--password=] <password> -h [--host=] <host>')
        sys.exit(2)

    # Open the connection to the Database
    client = InfluxDBClient(host, port, user, password, database)
    
    while True:
        print("Executing new speedtest...")
        # Execute the speedtest
        ping, download, upload = speedtest()
        # Upload data to DB
        upload_to_db(client, download, upload, ping)
        time.sleep(time_interval)

if __name__ == "__main__":
   main(sys.argv[1:])