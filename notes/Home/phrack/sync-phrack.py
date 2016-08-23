#! /usr/bin/env python
# coding: utf-8


import os
import sys
import datetime
import requests


PWD = os.path.split(os.path.realpath(__file__))[0]
VOLUME_URL = "http://www.phrack.org/archives/issues/%s/"
ISSUE_URL = "http://www.phrack.org/archives/issues/%s/%s.txt"

ZIM_HEADER = """Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.4
Creation-Date: %s

====== phrack volume %d issue %d======
Created %s

"""

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def issue_exists(volume, issue):
    path = "%s/volume%d/issue%d.txt" % (PWD, volume, issue)
    if os.path.exists(path):
        return True
    else:
        return False


def create_issue(content, volume, issue):
    path = "%s/volume%d" % (PWD, volume)
    if not os.path.exists(path):
        os.makedirs(path)
    path = "%s/volume%d/issue%d.txt" % (PWD, volume, issue)
    with open(path, "w") as issue_file:
        issue_file.write(ZIM_HEADER % (now, volume, issue, now))
        issue_file.write(content)


def sync():
    for volume in xrange(1, sys.maxint):
        resp = requests.head(VOLUME_URL % volume)
        if not resp.ok:
            # volume does not exist
            break
        for issue in xrange(1, sys.maxint):
            if issue_exists(volume, issue):
                continue
            print "Downloading: volume %d issue %d" % (volume, issue)
            resp = requests.get(ISSUE_URL % (volume, issue))
            if resp.ok:
                create_issue(resp.content, volume, issue)
            else:
                # issue does not exist
                break


def main():
    sync()


if __name__ == "__main__":
    main()
