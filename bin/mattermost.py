#!/usr/bin/python3
import argparse
import sys
import json
from requests import get, post, put
from datetime import datetime
from pprint import pprint

def main():
    ## arguments
    parser = argparse.ArgumentParser(description='push events to mattermost webhook')
    parser.add_argument('-u', type=str, dest='url', required=True, help='the url to mattermost webhook')
    args = parser.parse_args()
    # read event
    data = sys.stdin.read()
    status_readable = ['OK', 'Warning', 'Critical']
    # create json obj from event
    obj = json.loads(data)
    history = "history: "
    if obj['check']['history'] is not None:
        previous_hist = None
        for hist in obj['check']['history']:
            if previous_hist is None:
                dt = datetime.fromtimestamp(hist['executed'])
                history = history + "status: " + status_readable[hist['status']] + " " + str(dt) + ", "
            elif previous_hist['status'] != hist['status']:
                dt = datetime.fromtimestamp(hist['executed'])
                history = history + "status: " + status_readable[hist['status']] + " " + str(dt) + ", "
            previous_hist = hist
        message = obj['entity']['system']['hostname'] + ": " + obj['check']['output'] + " " + history 
    else:
        message = obj['entity']['system']['hostname'] + ": " + obj['check']['output']
    event = {"text": message}
    r = post(args.url, data=json.dumps(event))

if __name__ == '__main__':
    main()
