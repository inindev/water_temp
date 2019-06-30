#
# date_convert.py
#
#   utility for converting human readable date
#   string "2019-06-30 10:58:12" to its unix
#   epoch 1561892292 format
#
#   John Clark, 2019
#

from datetime import datetime, timezone
import sys


# convert date string as epoch date: 2019-06-30 10:58:12 -> 1561892292
def datestr_to_epoch(datestr):
    utc = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    utc_epoch = int(utc.timestamp())
    return utc_epoch


def main(argv):
    if len(argv) != 2:
        print('usage: python3 {} "YYYY-MM-DD HH:MM:SS"\n'.format(argv[0]))

    datestr = argv[1]
    epoch = datestr_to_epoch(datestr)
    print('{} -> {}'.format(datestr, epoch))



if __name__ == '__main__':
    main(sys.argv)
