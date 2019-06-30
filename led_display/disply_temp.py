
from TM1637 import TM1637
import sys
sys.path.append('..')
import my_config


with open(my_config.LOG_PATH_LAST, 'r') as fp:
    ll = list(fp)[-1]

vals = ll.split("\t")
temp_c1000 = int(vals[1])
temp_f = float(temp_c1000) * 9.0 / 5000.0 + 32.0

disp = TM1637(gpio_clk=17, gpio_dio=18)
str = '{:.1f}'.format(temp_f)
print(str)
disp.set_string(str)

