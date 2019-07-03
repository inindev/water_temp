#
# show_temps.py
#
#   python utility for displaying the previous 100
#   temperature readings in human readable format
#
#   John Clark, 2019
#

from datetime import datetime, timezone, timedelta
import os, sys
import my_config

# EDT or EST
tz_offs = timedelta(hours=4 if os.popen('TZ="US/Eastern" date +%z').read().strip()=='-0400' else 5)


def read_file(file):
    arr = None
    with open(file, 'r') as fp:
        arr = list(fp)
    return arr


def datestr_to_eastern(datestr):
    utc = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    local = utc - tz_offs
    ap = 'p' if local.strftime('%p') == 'PM' else 'a'
    eastern = local.strftime('%-m/%-d/%Y %I:%M{}').format(ap)
    return eastern


def c1000_to_fahrenheit(temp_c1000):
    temp_f10 = round(float(temp_c1000) * 9.0 / 500.0 + 320.0)
    return temp_f10 / 10.0


def entry_to_disp(entry):
    tokens = entry.split('\t')
    date = datestr_to_eastern(tokens[0])
    temp = c1000_to_fahrenheit(tokens[1])
    disp = '{} -> {:.1f}'.format(date, temp)
    return disp


def main():
    arr = read_file(my_config.path.log)
    for entry in arr[-100:]:
        disp = entry_to_disp(entry)
        print(disp)



if __name__ == '__main__':
    if sys.version_info.major < 3:
        print('python 3 required')
        sys.exit(1)
    main()

