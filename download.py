#! /usr/bin/env python3
"""Bulk download LangagePod101 RSS feed items.

For reference, as of 2017-12-02 JapanesePod101 has over 9000+ items,
3+ formats (mp4 video, mp3 audio, pdf text), over 4+ different file
hosts (AWS S3, cloudfront, jp101, libsyn) with dates going back 12
years (2005 - 2017). Full archives are about 45.3 GB.
"""
from datetime import datetime
import importlib
import logging
from multiprocessing.dummy import Pool as ThreadPool
import os
import random
import re
import requests
import shutil
import sys
import threading
import time
import xml.etree.ElementTree as ElementTree

headers = {
    'user-agent': 'iTunes/12.9.5 (Macintosh; OS X 10.14.6) AppleWebKit/607.3.9'
}

# Parse parameters.
if len(sys.argv) != 2:
    print('Usage: python3 download.py [PYTHON_PARAMETERS_FILE]')
    exit()
params_file = sys.argv[1].split('.')[0]
params = importlib.import_module(params_file)

credentials = params.credentials
rss_url = re.sub('itpc', 'https', params.rss_url)
output_dir = params.output_dir
num_threads = params.num_threads if 0 < params.num_threads <= 6 else 4

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

# Define global variables.
topic = None
try:
    topic = re.search('www\.(.*)\.com', rss_url).group(1)
except Exception:
    print('Error: {} is not a valid URL'.format(rss_url))
    exit()
rss_cache = topic + '.xml'
if not os.path.isfile(rss_cache):
    response = requests.get(rss_url, auth=credentials, headers=headers)
    with open(rss_cache, 'w') as f:
        f.write(response.text)

tree = ElementTree.parse(rss_cache)
items = tree.getroot().findall('./channel/item')
num_items = len(items)

logpath = os.path.join(output_dir, 'download.log')
logging.basicConfig(filename = logpath, level = logging.DEBUG)

count_lock = threading.Lock()
count = 1

now = datetime.now().timestamp()

def download_item(item):
    title = item.find('title').text
    title_clean = re.sub('/', '_', title)
    pubdate = item.find('pubDate').text
    url = item.find('enclosure').attrib['url']

    orig_filename = url.split('/')[-1]
    orig_ext = orig_filename.split('.')[-1]
    filename = '{}.{}'.format(title_clean, orig_ext)
    outpath = os.path.join(output_dir, filename)

    access_time = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z").timestamp()

    global count
    with count_lock:
        logging.info('{}/{}: {} -> {} + {}'.format(count, num_items, url, outpath, access_time))
        count += 1

    if os.path.isfile(outpath) and os.path.getsize(outpath) > 0:
        logging.info(outpath + ' already exists, skipping.')
        return

    try:
        response = None
        if 'amazonaws' in url:
            response = requests.get(url, stream=True, headers=headers)
        else:
            response = requests.get(url, auth=credentials, stream=True, headers=headers)

        response.raise_for_status()
        with open(outpath, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        os.utime(outpath, (access_time, access_time))
    except Exception:
        logging.error("Failed to download file", exc_info=True)

    # Avoid overburdening the file server.
    time.sleep(0.25 + random.uniform(-0.15, 0.25))


pool = ThreadPool(num_threads)
pool.map(download_item, items)
pool.close()
pool.join()
