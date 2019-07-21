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
    temp_c1000w = read_temp_c1000(my_config.therm.w)
    temp_c1000a = read_temp_c1000(my_config.therm.a)
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(0.4)
    temp_c1000w = read_temp_c1000(my_config.therm.w)
    temp_c1000a = read_temp_c1000(my_config.therm.a)

    totalw = 0
    totala = 0
    for x in range(8):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.4)
        temp_c1000w = read_temp_c1000(my_config.therm.w)
        temp_c1000a = read_temp_c1000(my_config.therm.a)
        totalw += temp_c1000w
        totala += temp_c1000a
    print()

    dtnow = datetime.utcnow().replace(microsecond=0)
    avg_c1000w = float(totalw) / 8.0
    avg_c1000a = float(totala) / 8.0
    c1000w = round(avg_c1000w)
    c1000a = round(avg_c1000a)
    temp_fw = avg_c1000w * 9.0 / 5000.0 + 32.0
    temp_fa = avg_c1000a * 9.0 / 5000.0 + 32.0
    print('{}  water: {} ({:.1f})  air: {} ({:.1f})'.format(dtnow, c1000w, temp_fw, c1000a, temp_fa))
    with open(my_config.path.log, 'a') as fp:
        fp.write('{}\tw:{}\ta:{}\n'.format(dtnow, c1000w, c1000a)) # water, air

    with open(my_config.path.upload, 'a') as fp:
        fp.write('{}\tw:{}\ta:{}\n'.format(dtnow, c1000w, c1000a))



if __name__ == '__main__':
    if sys.version_info.major < 3:
        print('python 3 required')
        sys.exit(1)
    main()
