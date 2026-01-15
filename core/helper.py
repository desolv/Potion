from datetime import datetime, timedelta

import pytz


def retrieve_current_formatted_time(
    datetime_format: str = "%d %B %Y %H:%M",
    timezone: str = "Europe/London",
) -> str:
    """
    Return the current time formatted
    :param datetime_format:
    :param timezone:
    :return:
    """
    now = datetime.now(pytz.timezone(timezone))
    return now.strftime(datetime_format)


def retrieve_current_time_with_timezone(timezone: str = "Europe/London") -> datetime:
    """
    Return the current datetime in the specified timezone
    :param timezone:
    :return:
    """
    tz = pytz.timezone(timezone)
    return datetime.now(tz)


def retrieve_current_time() -> datetime:
    """
    Return the current datetime
    :return:
    """
    return datetime.now()


def to_discord_timestamp(dt: datetime, style: str = "F") -> str:
    """
    Convert a datetime into a Discord timestamp
    style = t, T, d, D, F, R
    """
    unix_timestamp = int(dt.timestamp())
    return f"<t:{unix_timestamp}:{style}>"


def format_given_time(
    time: datetime,
    datetime_format: str = "%d/%m/%y %H:%M",
    timezone: str = "Europe/London",
) -> str:
    """
    Render a datetime in the given timezone - Treated as UTC
    :param time:
    :param datetime_format:
    :param timezone:
    :return:
    """
    target_tz = pytz.timezone(timezone)
    if time.tzinfo is None:
        aware = pytz.utc.localize(time)
    else:
        aware = time.astimezone(pytz.utc)
    return aware.astimezone(target_tz).strftime(datetime_format)


def parse_duration(duration_str: str) -> timedelta:
    """
    Parse duration string into timedelta
    Supported formats: 10s, 5m, 2h, 1d
    :param duration_str:
    :return:
    """
    duration_str = duration_str.lower().strip()

    if len(duration_str) < 2:
        raise ValueError("Duration too short")

    unit = duration_str[-1]
    try:
        value = int(duration_str[:-1])
    except ValueError:
        raise ValueError("Invalid duration format. Use format like: 10s, 5m, 2h, 1d")

    if value <= 0:
        raise ValueError("Duration must be positive")

    if unit == "s":
        return timedelta(seconds=value)
    elif unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    else:
        raise ValueError(f"Unknown unit: {unit}. Use s, m, h, or d")
