Python3 scripts written hastily prior to a lengthy plane trip in order to:
* bulk download RSS feed items from LanguagePod101 sites.
* organize downloaded files into subfolders according to subject.

The script downloads everything available in a LanguagePod101 RSS feed, including audio, video, and PDF notes. Should work on any LanguagePod101 site, including JapanesePod101, ChineseClass101 and SpanishPod101.

If the download script is interrupted, it can be resumed. The downloader uses four threads by default, feel free to tweak as needed.

**NOTE**: While this should work for free LanguagePod101 accounts, a *paid* account is typically required to access the full archives.

Requirements
===
* Python 3 (easily portable to Python 2 if you really need to)
* requests (`pip3 install requests`)
* an account on a LanguagePod101 site
* enough free disk space to download the feed (examples: 45.3 GB for JapanesePod101 as of 2017-12, 5.5 GB for UrduPod101)

Usage
===
# Download
1. Fill in `parameters.py` with your download target and account information.
1. Run the download script: `python3 download.py parameters.py`. This could take a few hours depending on the size of the archives and the speed of your connect. If for any reason the script is interrupted before completion, just run it again and it will resume from where it left off. Resuming will skip any files which were already downloaded.
1. Check the `download.log` in your output path for `ERROR`s. A few errors is normal, especially in older feeds like JapanesePod101 which contain some dead links.
# Organize (optional)
1. After downloading is complete, run the organize script: `python3 organize.py parameters.py`. Your files will be organized into subfolders according to subject.
1. Check the `organize.log` in your output path for `ERROR`s. There shouldn't be any, but a few is probably OK.
1. Typically a few files have inconsistent or malformed filenames and thus are not auto-organized. You can organize these manually by fixing whatever is inconsistent with the filenames, then either run `organize.py` again or manually move the files to their correct folders.

License
==
This source code is released under the Mozilla Public License 2.0.

To Coders
===
These scripts can be reused to bulk download and organize other RSS feeds with little modification. You will mostly need to change which RSS `<item>` fields are used by the `download.py:download_item()` function to generate filenames, then alter `organize.py` to follow your chosen file naming scheme.

If you create a project based on this code, I'd love to hear about it!

To Everyone
===
I am in no way affiliated with LanguagePod101, just love their content and want to make it easier for paid subscribers to manage the large and sometimes unwieldy archives which many podcast downloaders choke on. Try bulk downloading early episodes of JapanesePod101 on a mobile device and you'll see what I mean.
