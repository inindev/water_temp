#
# upload_s3.py
#
#   utility for uploading the latest reading to s3 via boto
#
#   John Clark, 2019
#

import boto3
from datetime import datetime, timezone
import sys
import json
import my_config


def get_last_n_entries(file, n):
    last = None
    with open(file, 'r') as fp:
        last = list(fp)[-n:]
    return last


def c1000_to_fahrenheit(temp_c1000):
    temp_f10 = round(float(temp_c1000) * 9.0 / 500.0 + 320.0)
    return temp_f10 / 10.0


# parses a log data entry and returns json
#   input:  2019-06-30 20:21:22   w:29636   a:28032
#   output: {'date': '2019-06-30 20:21:22', 'epoch': 1561926082, 'c1000w': 29636, 'tempw': 85.3, 'c1000a': 28032, 'tempa': 82.5}
def parse_line(line):
    tokens = line.split('\t')
    if len(tokens) != 3:
        return None

    # extract date as epoch date: 1561811080
    date = tokens[0]
    utc = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    utc_epoch = int(utc.timestamp())
    # extract temps as raw celsius * 1000
    temp_c1000w = int(tokens[1][2:])
    temp_fw = c1000_to_fahrenheit(temp_c1000w)
    temp_c1000a = int(tokens[2][2:])
    temp_fa = c1000_to_fahrenheit(temp_c1000a)

    data = {
        'date':   date,
        'epoch':  utc_epoch,
        'c1000w': temp_c1000w,
        'tempw':  temp_fw,
        'c1000a': temp_c1000a,
        'tempa':  temp_fa
    }

    return data


def s3_upload_json(region, bucket, file, data):
    data_json = json.dumps(data)
    print('storing: {}'.format(data_json))
    s3 = boto3.resource('s3', region_name=region)
    s3file = s3.Object(bucket, file)
    s3file.put(Body=data_json.encode('utf8'), ContentType='application/json', ACL='public-read')


def main():
    entries = get_last_n_entries(my_config.path.log, 5)
    if not entries:
        print('no entries found')
        sys.exit(1)

    data = []
    for entry in entries:
        line = parse_line(entry)
        if line:
            data.append(line)

    s3_upload_json(my_config.aws.region,
                   my_config.aws.s3.bucket,
                   my_config.aws.s3.file,
                   data)



if __name__ == '__main__':
    if sys.version_info.major < 3:
        print('python 3 required')
        sys.exit(1)
    main()
