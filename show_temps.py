
from datetime import datetime, timezone, timedelta
import os
import my_config

tz_off = timedelta(hours=4) if os.popen('TZ="US/Eastern" date +%z').read().strip() == '-0400' else timedelta(hours=5)

with open(my_config.LOG_PATH, 'r') as fp:
    ll = list(fp)

n = len(ll)
n100 = max(0, n - 100)

print('showing reading nums: {} -> {}'.format(n100, n))
for i in range(n100, n):
    tokens = ll[i].split('\t')

    utc = datetime.strptime(tokens[0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    local = utc - tz_off
    ap = 'p' if local.strftime('%p') == 'PM' else 'a'
#    date = local.strftime('%I:%M{} %-m/%-d/%Y').format(ap)
    date = local.strftime('%-m/%-d/%Y %I:%M{}').format(ap)

    temp_c1000 = float(tokens[1])
    temp_f = temp_c1000 * 9.0 / 5000.0 + 32.0

    print('{} -> {:.1f}'.format(date, temp_f))

