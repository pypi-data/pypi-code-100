import datetime


def hasRunToday():
    now = datetime.datetime.now()

    try:
        with open("lastSent", "r") as lastSentFile:
            lastSent = datetime.datetime.strptime(lastSentFile.read(), '%Y-%m-%d')

            dateDiff = (now - lastSent)

            if dateDiff.days < 1:
                return True
    except:
        pass

    # Write date in file
    with open("lastSent", "w") as lastSentFile:
        lastSentFile.write(str(now.date()))

    return False
