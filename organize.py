#! /usr/bin/env python3
'''Organize LanguagePod101 folders post-download.
Each subject is given a folder.'''
import glob
import importlib
import logging
import os
import shutil
import sys

# Parse parameters.
if len(sys.argv) != 2:
    print('Usage: python3 organize.py [PYTHON_PARAMETERS_FILE]')
    exit()
params_file = sys.argv[1].split('.')[0]
params = importlib.import_module(params_file)

path = params.output_dir

logpath = os.path.join(path, 'organize.log')
logging.basicConfig(filename = logpath, level = logging.DEBUG)

# Gather subject map (key: subject, value: num items).
# Filenames assumed to have regex form: ^(.*) \#.*$
# where capture group is subject.
subjects = {}
for filename in glob.glob(path + '*'):
    if os.path.isdir(filename):
        continue
    nameparts = filename.split(' #')
    if len(nameparts) == 1:
        logging.info('No part number in name: {}'.format(filename))
        continue
    subject = nameparts[0]
    if subject in subjects:
        subjects[subject] += 1
    else:
        subjects[subject] = 1

# Move items to their subject folders.
for subject in subjects.keys():
    filenames = glob.glob(subject + ' #*')
    print(filenames)
    if not os.path.isdir(subject):
        os.makedirs(subject)
    for filename in filenames:
        shutil.move(filename, subject)

# The few remaining files should be hand sorted.
