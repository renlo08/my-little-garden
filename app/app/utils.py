from datetime import datetime, timezone, timedelta


def arrange_urlpatterns(urlpatterns_list):
    general_urlpatterns = []
    specific_urlpatterns = []

    for pattern in urlpatterns_list:
        if '<' in pattern.pattern.regex.pattern:  # This means it's a general pattern
            general_urlpatterns.append(pattern)
        else:
            specific_urlpatterns.append(pattern)

    return specific_urlpatterns + general_urlpatterns


def compute_time_difference(date: datetime):
    current_time = datetime.now(tz=timezone.utc)  # This is timezone-aware
    time_difference = current_time - date

    if time_difference < timedelta(minutes=1):
        return f"il y a moins d´une minute."
    elif time_difference < timedelta(hours=1):
        minutes = int(time_difference.total_seconds() / 60)
        return f"il y a {minutes}min."
    elif time_difference < timedelta(days=1):
        hours = int(time_difference.total_seconds() // 3600)
        return f"il y a {hours}h."
    else:
        return f"il y a {time_difference.days}j."
