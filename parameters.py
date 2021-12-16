from datetime import datetime, timedelta, timezone

# Path to download files to. Can be relative.
output_dir = ''
# RSS feed URL. Can be http or itpc.
rss_url = ''
# Replace USERNAME and PASSWORD with your LanguagePod101 credentials.
credentials = ('USERNAME', 'PASSWORD')
# Number of download threads.
# Must be greater than 0 and less than or equal to 6.
# Each thread downloads a different file. Decrease
# if you have a slow internet connection or have fewer CPU cores on your
# machine.
num_threads = 4
# Cutoff dates to filter downloads by.
tz = timezone(-timedelta(hours=8))
start_date = datetime(1000, 1, 1, tzinfo=tz)
end_date = datetime(3000, 1, 1, tzinfo=tz)
