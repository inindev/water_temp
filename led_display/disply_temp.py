#
# date_convert.py
#
#   utility for reading the last temperature log
#   entry and displaying it on a TM1637 LED display
#   rpi pins gpio_clk=17, gpio_dio=18
#
#   John Clark, 2019
#

from TM1637 import TM1637
import sys
sys.path.append('..')
import my_config


def get_last_entry(file):
    last = None
    with open(file, 'r') as fp:
        last = list(fp)[-1]
    return last


def c1000_to_fahrenheit(temp_c1000):
    temp_fahrenheit = float(temp_c1000) * 9.0 / 5000.0 + 32.0
    return temp_fahrenheit


def main():
    entry = get_last_entry(my_config.LOG_PATH)
    tokens = entry.split('\t')
    temp = c1000_to_fahrenheit(tokens[1])
    temp_str = '{:.1f}'.format(temp)

    disp = TM1637(gpio_clk=17, gpio_dio=18)
    disp.set_string(temp_str)
    print(temp_str)


if __name__ == '__main__':
    main()

