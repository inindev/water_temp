#
# date_convert.py
#
#   utility for converting human readable date
#   string "2019-06-30 10:58:12" to its unix
#   epoch 1561892292 format
#
#   John Clark, 2019
#

from datetime import datetime, timezone, timedelta
import os, sys


# convert date string to epoch date: 2019-06-30 10:58:12 -> 1561892292
def datestr_to_epoch(datestr):
    utc = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    utc_epoch = int(utc.timestamp())
    return utc_epoch

# convert epoch date to date string: 1561911358 -> 2019-06-30 16:15:58 UTC
def epoch_to_datestr(epoch, eastern):
    datestr = None
    utc = datetime.fromtimestamp(int(epoch)).astimezone(timezone.utc)
    if eastern:
        # EDT or EST
        edt = os.popen('TZ="US/Eastern" date +%z').read().strip() == '-0400'
        local = utc - timedelta(hours=4 if edt else 5)
        datestr = local.strftime('%Y-%m-%d %H:%M:%S {}'.format('EDT' if edt else 'EST'))
    else:
        datestr = utc.strftime('%Y-%m-%d %H:%M:%S UTC')

    return datestr


def main(argv):
    argc = len(argv)
    if argc < 2 or argc > 3:
        print('usage: python3 {} "nnnnnnnnnn"\n'.format(argv[0]))
        print('       python3 {} "YYYY-MM-DD HH:MM:SS"\n'.format(argv[0]))

    arg = argv[1]
    arglen = len(arg)
    if arglen == 10:
        res = epoch_to_datestr(arg, argc==3)
        print('{} -> {}'.format(arg, res))
    elif arglen == 19:
        res = datestr_to_epoch(arg)
        print('{} -> {}'.format(arg, res))
    else:
        print('unrecognized date format: {}'.format(arg))



if __name__ == '__main__':
    if sys.version_info.major < 3:
        print('python 3 required')
        sys.exit(1)
    main(sys.argv)
