import datetime



current_time_utc = datetime.datetime.now(datetime.timezone.utc)
south_africa_tz = datetime.timezone(datetime.timedelta(hours=2))
print("Current UTC time:", current_time_utc)