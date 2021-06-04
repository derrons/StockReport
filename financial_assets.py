import datetime

# method to validate that import file header matches expected hearder list
def validate_header(primary, secondary) -> bool:
    notmatch = []
    a = [x.lower() for x in primary]
    for b in secondary:
        if b.lower() not in a:
            notmatch.append(b)
    return len(primary) == len(secondary) and len(notmatch) == 0

# method to validate text is an integer value
def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except:
        return False

# method to validate text is a floating value
def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except:
        return False

# method to validate text is a valid date
def is_date(value: str) -> bool:
    try:
        dates = value.split('/')
        datetime.datetime(int(dates[2]), int(dates[0]), int(dates[1]))
        return True
    except:
        return False