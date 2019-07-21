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
import os, sys
#import glob
import time
import sys
import my_config


def read_temp_c1000(device):
    cal = my_config.therm.cal[device]
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
    temp_c1000a = read_temp_c1000(my_config.therm.a)
    temp_c1000b = read_temp_c1000(my_config.therm.b)
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(0.4)
    temp_c1000a = read_temp_c1000(my_config.therm.a)
    temp_c1000b = read_temp_c1000(my_config.therm.b)

    totala = 0
    totalb = 0
    for x in range(8):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.4)
        temp_c1000a = read_temp_c1000(my_config.therm.a)
        temp_c1000b = read_temp_c1000(my_config.therm.b)
        totala += temp_c1000a
        totalb += temp_c1000b
    print()

    dtnow = datetime.utcnow().replace(microsecond=0)
    avg_c1000a = float(totala) / 8.0
    avg_c1000b = float(totalb) / 8.0
    c1000a = round(avg_c1000a)
    c1000b = round(avg_c1000b)
    temp_fa = avg_c1000a * 9.0 / 5000.0 + 32.0
    temp_fb = avg_c1000b * 9.0 / 5000.0 + 32.0
    print('{}  water: {} ({:.1f})  air: {} ({:.1f})'.format(dtnow, c1000a, temp_fa, c1000b, temp_fb))
    with open(my_config.path.log, 'a') as fp:
        fp.write('{}\tw:{}\ta:{}\n'.format(dtnow, c1000a, c1000b)) # water, air

    with open(my_config.path.upload, 'a') as fp:
        fp.write('{}\tw:{}\ta:{}\n'.format(dtnow, c1000a, c1000b))



if __name__ == '__main__':
    if sys.version_info.major < 3:
        print('python 3 required')
        sys.exit(1)
    main()
