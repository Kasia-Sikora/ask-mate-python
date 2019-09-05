from datetime import datetime, time


def utc_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


