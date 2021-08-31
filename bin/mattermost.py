#!/usr/bin/python
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
    lines = sys.stdin.readlines()
    data = ""
    for line in lines:
        data = data.join(line)
    # create json obj from event
    obj = json.loads(data)
    history = "history: "
    if obj['check']['history'] is not None:
        previous_hist = None
        for hist in obj['check']['history']:
            if previous_hist & previous_hist['status'] != hist['status']:
                dt = datetime.fromtimestamp(hist['executed'])
                history = history + "status: " + str(hist['status']) + " " + str(dt) + ", \n"
            previous_hist = hist
        message = obj['entity']['system']['hostname'] + ": " + obj['check']['output'] + " " + history 
    else:
        message = obj['entity']['system']['hostname'] + ": " + obj['check']['output']

    event = {"text": message}
    r = post(args.url, data=json.dumps(event))

if __name__ == '__main__':
    main()
