
from datetime import datetime, timezone
import os
import json
import urllib.request as request
import my_config


def read_file(file):
    arr = None
    with open(file, 'r') as fp:
        arr = list(fp)
    return arr


def write_file_remove(file, arr):
    with open(file, 'w') as fp:
        fp.writelines(arr[1:])


def get_head(arr):
    if len(arr) < 1:
        return None
    line = arr[0].strip()
    return line


def parse_line(line):
    tokens = line.split('\t')
    if len(tokens) != 2:
        return None

    # extract date as epoch date: 1561811080
    utc = datetime.strptime(tokens[0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    utc_epoch = int(utc.timestamp())
    # extract temps as raw celsius * 1000 
    temp_c1000 = int(tokens[1])

    data = {
        "date": utc_epoch,
        "temp": temp_c1000
    }

    return data


def aws_upload_data(url, key, data):
    print('sending: {}'.format(data))
    data_json = json.dumps(data)
    
    req = request.Request(url=url, data=data_json.encode('utf-8'), method='POST')
    req.add_header("content-type", "application/json")
    req.add_header("x-api-key", key)
    
    resp = request.urlopen(req)
    resp_str = resp.read().decode('utf-8')
    resp_json = json.loads(resp_str)
    print('response: {}'.format(resp_json))

    code = resp_json['statusCode']
    if code != 200:
        print('error, statusCode: {}'.format(code))
        return code

    resp_data = resp_json['data']
    if data['date'] != resp_data['epoch']:
        print('error, response data.date - sent: {} received: {}'.format(data['date'], resp_data['epoch']))
        return -1

    if data['temp'] != resp_data['temp']:
        print('error, response data.temp - sent: {} received: {}'.format(data['temp'], resp_data['temp']))
        return -2

    return 0;


def process_top_entry(file):
    arr = read_file(file)
    if not arr:
        print('file empty')
        return 0

    line = get_head(arr)
    if not line:
        print('discarding empty line')
        write_file_remove(file, arr)
        return 0

    data = parse_line(line)
    if not data:
        print('failed to parse line: [{}]'.format(line))
        print('discarding corrupt line')
        write_file_remove(file, arr)
        return 1 # error, bad parse

    rc = aws_upload_data(my_config.AWS_URL, my_config.API_KEY, data)
    if rc != 0:
        return -1 # error, bad upload

    # line successfully uploaded, remove from file
    write_file_remove(file, arr)
    return 0


def main():
    while os.stat(my_config.LOG_PATH_LAST).st_size > 0:
        rc = process_top_entry(my_config.LOG_PATH_LAST)
        if rc < 0:
            return


main()

