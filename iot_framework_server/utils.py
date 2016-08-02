import time, datetime


def timestamp_to_datetime(timestamp):
    s, ms = divmod(timestamp, 1000)
    # print("%s -> %s, %s" % (timestamp, s, ms))
    return '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s)), ms)
    # return datetime.datetime.fromtimestamp(
    #     timestamp
    # ).strftime('%Y-%m-%d %H:%M:%S')
