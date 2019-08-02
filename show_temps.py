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


# input:  2019-08-02 09:21:22	w:28250	a:22345
# output: 2019-08-02 05:21:22  ->  water: 82.9°  air: 72.2°
def entry_to_disp(entry):
    tokens = entry.split('\t')
    if len(tokens) != 3:
        return None

    date = datestr_to_eastern(tokens[0])

    # tokens are celsius * 1000
    temp_c1000w = int(tokens[1][2:])
    temp_fw = c1000_to_fahrenheit(temp_c1000w)
    temp_c1000a = int(tokens[2][2:])
    temp_fa = c1000_to_fahrenheit(temp_c1000a)

    disp = '{}  ->  water: {:.1f}°  air: {:.1f}°'.format(date, temp_fw, temp_fa)
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
