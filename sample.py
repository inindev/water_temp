#
# sample.py
#
#   python utility for sampling temperature thermistor
#   thermistor values are in celsius * 1000
#
#   readings taken by averaging 8 readings from two thermistors
#   two priming readings are taken before sample series
#
#   John Clark, 2019
#

from datetime import datetime
import os
#import glob
import time
import sys
import my_config


THERM_A = '28-000008afdc2d'
THERM_B = '28-000008b06dc7'

#CAL = {'28-000008afdc2d':-139, '28-000008b06dc7':18}
#CAL = {'28-000008afdc2d':-463, '28-000008b06dc7':-463}
CAL = { '28-000008afdc2d': -100,
        '28-000008b06dc7': +60 }


def read_temp_c1000(device):
    cal = CAL[device]
    path = '/sys/bus/w1/devices/{}/w1_slave'.format(device)
    with open(path, 'r') as fp:
        for i in range(3):
            lines = fp.readlines()
            if lines[0].strip()[-3:] == 'YES':
                equals_pos = lines[1].find('t=')
                if equals_pos != -1:
                    temp_c1000 = int(lines[1][equals_pos+2:]) + cal
                    return temp_c1000
            time.sleep(0.2)


def main():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

#    devices = [os.path.basename(dp) for dp in glob.glob('/sys/bus/w1/devices/28*')]
    temp_c1000a = read_temp_c1000(THERM_A)
    temp_c1000b = read_temp_c1000(THERM_B)
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(0.4)
    temp_c1000a = read_temp_c1000(THERM_A)
    temp_c1000b = read_temp_c1000(THERM_B)

    total = 0
    for x in range(8):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.4)
        temp_c1000a = read_temp_c1000(THERM_A)
        temp_c1000b = read_temp_c1000(THERM_B)
        total = total + temp_c1000a + temp_c1000b
    print()

    dtnow = datetime.utcnow().replace(microsecond=0)
    avg_c1000 = float(total) / 16.0
    c1000 = round(avg_c1000)
    temp_f = avg_c1000 * 9.0 / 5000.0 + 32.0
    print('{}  {} ({:.1f})'.format(dtnow, c1000, temp_f))
    with open(my_config.path.log, 'a') as fp:
        fp.write('{}\t{}\n'.format(dtnow, c1000))

    with open(my_config.path.upload, 'a') as fp:
        fp.write('{}\t{}\n'.format(dtnow, c1000))



if __name__ == '__main__':
    main()

