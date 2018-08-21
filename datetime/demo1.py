from datetime import datetime
from  datetime import date
from  datetime import timezone,timedelta
dt = datetime(2015, 4, 19, 12, 20)
print(datetime.now().year)
print(dt.utcfromtimestamp)
print(dt.minute)
print(datetime.today())
print(dt.weekday())

print(dt.ctime())
print(dt.timetuple()[0])
#print(dt.toordinal())
cday = datetime.strptime('2018-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday.year)

utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_dt)

#! /usr/bin/python
# coding=utf-8

from datetime import datetime, tzinfo,timedelta

"""
tzinfo是关于时区信息的类
tzinfo是一个抽象类，所以不能直接被实例化
"""
class UTC(tzinfo):
    """UTC"""
    def __init__(self,offset = 0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)

#北京时间
beijing = datetime(2011,11,11,0,0,0,tzinfo = UTC(8))
#曼谷时间
bangkok = datetime(2011,11,11,0,0,0,tzinfo = UTC(7))

#北京时间转成曼谷时间
beijing.astimezone(UTC(7))
#计算时间差时也会考虑时区的问题
timespan = beijing - bangkok
