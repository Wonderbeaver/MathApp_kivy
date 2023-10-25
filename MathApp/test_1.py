def milliseconds_to_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 100)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    time_format = "{:02}:{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds), int(milliseconds))
    return time_format

if __name__ == "__main__":
    print(milliseconds_to_time(19))