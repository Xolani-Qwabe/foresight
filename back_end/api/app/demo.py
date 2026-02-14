import datetime
import pytz



current_time_utc = datetime.datetime.now(pytz.timezone('Africa/Johannesburg'))
print("Current UTC time:", current_time_utc)