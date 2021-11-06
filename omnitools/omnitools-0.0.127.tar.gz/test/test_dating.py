from omnitools import rfc822gmt2dt, dt2rfc822gmt, dt2yyyymmddhhmmss
from dateutil.tz import tzlocal, tzoffset
import datetime


now_m8 = datetime.datetime.now(tz=tzoffset(None, -28800))
now = datetime.datetime.now(tz=tzoffset(None, 0))
now_p8 = datetime.datetime.now(tz=tzoffset(None, 28800))
print(dt2yyyymmddhhmmss(now_m8))
print(dt2rfc822gmt(now_m8))
test_m8 = rfc822gmt2dt(dt2rfc822gmt(now_m8))
print(now_m8, now_m8.timestamp())
print(test_m8, test_m8.timestamp())
print()
print(dt2yyyymmddhhmmss(now))
print(dt2rfc822gmt(now))
test = rfc822gmt2dt(dt2rfc822gmt(now))
print(now, now.timestamp())
print(test, test.timestamp())
print()
print(dt2yyyymmddhhmmss(now_p8))
print(dt2rfc822gmt(now_p8))
test_p8 = rfc822gmt2dt(dt2rfc822gmt(now_p8))
print(now_p8, now_p8.timestamp())
print(test_p8, test_p8.timestamp())
print()
print(now > now_m8, now > now_p8)
print(now < now_m8, now < now_p8)
print(now == now_m8, now == now_p8)
