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
    status_icon = [':large_green_circle:', ':large_orange_circle:', ':red_circle:']
    # create json obj from event
    obj = json.loads(data)
    formatted_history = ""
    if obj['check']['history'] is not None:
        previous_hist = None
        history = []
        for hist in obj['check']['history']:
            if previous_hist is None:
                dt = datetime.fromtimestamp(hist['executed'])
                history.append(str(dt) + ": " + status_readable[hist['status']] )
            elif previous_hist['status'] != hist['status']:
                dt = datetime.fromtimestamp(hist['executed'])
                history.append(str(dt) + ": " + status_readable[hist['status']] )
            previous_hist = hist
        if len(history) > 5:
            formatted_history = "history: \n ```\n" + "\n".join(history[-5::-1]) + "\n```\n"
        else:
            formatted_history = "history: \n ```\n" + "\n".join(history[::-1]) + "\n```\n"
    curr_status = hist['status']
    message = " **" + obj['entity']['system']['hostname'] + ": " + status_readable[curr_status] + "**  " + status_icon[curr_status] + "\n\n"
    message = message + obj['check']['output']
    message = message + " " + formatted_history
    event = {"text": message}
    r = post(args.url, data=json.dumps(event))

if __name__ == '__main__':
    main()
