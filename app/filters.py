import time


def gen_time_str(date):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date))