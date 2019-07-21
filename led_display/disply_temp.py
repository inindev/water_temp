#
# display_temp.py
#
#   utility for reading the last temperature log
#   entry and displaying it on a TM1637 LED display
#   rpi pins gpio_clk=17, gpio_dio=18
#
#   John Clark, 2019
#

from TM1637 import TM1637
from datetime import datetime
import sys
import my_config


def get_last_entry(file):
    last = None
    with open(file, 'r') as fp:
        last = list(fp)[-1]
    return last


def c1000_to_fahrenheit(temp_c1000):
    temp_f10 = round(float(temp_c1000) * 9.0 / 500.0 + 320.0)
    return temp_f10 / 10.0


def can_show():
    dtnow = datetime.utcnow().replace(microsecond=0)

    # date_begin: april ->  4/1
    # date_end:   nov   -> 11/1
    can_show_month = (dtnow.month > 3) and (dtnow.month < 11)

    # time begin: 7:00a -> 11:00 UTC
    # time end:   8:00p -> 24:00 UTC
    can_show_hour = (dtnow.hour > 10) and (dtnow.hour < 24)

    return can_show_month and can_show_hour


def main():
    disp = TM1637(gpio_clk=17, gpio_dio=18)

    if not can_show():
        disp.brightness = 0
        print('blackout time, not showing...')
        return

    entry = get_last_entry(my_config.path.log)
    tokens = entry.split('\t')
    temp = c1000_to_fahrenheit(tokens[1][2:])
    temp_str = '{:.1f}'.format(temp)

    disp.brightness = 4
    disp.set_string(temp_str)
    print(temp_str)



if __name__ == '__main__':
    if sys.version_info.major < 3:
        print('python 3 required')
        sys.exit(1)
    main()
