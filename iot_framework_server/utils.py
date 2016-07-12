import time, datetime


def timestamp_to_datetime(timestamp):
    s, ms = divmod(1236472051807, 1000)
    return '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
    # return datetime.datetime.fromtimestamp(
    #     timestamp
    # ).strftime('%Y-%m-%d %H:%M:%S')
