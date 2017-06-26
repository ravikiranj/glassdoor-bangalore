#!/usr/bin/env python

import requests
import json

base_url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=<REDACTED>&t.k=<REDACTED>&action=employers&l=bangalore&country=india&userip=73.170.151.250&useragent=Mozilla/5.0"

def get_data_and_write_to_file(page_num):
    print "Fetching data for %d" % (page_num)
    url = base_url + "&pn=" + str(page_num)
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
    if r.status_code != 200:
        print "Non-200 HTTP Response, could not process, status_code = ", r.status_code
        print r.text
        return False

    resp = r.json()
    fname = "data/raw/%04d.json" % (page_num)
    print "Writing data to %s" % (fname)
    with open(fname, "w") as op:
        json.dump(resp, op, indent=4, sort_keys=True)
    return True

if __name__ == "__main__":
    ids = []
    with open("failed_ids.txt") as ip:
        for row in ip:
            ids.append(int(row.strip()))

    failed_ids = []
    for i in ids:
        status = get_data_and_write_to_file(i)
        if not status:
            failed_ids.append(i)

    with open("failed_ids.txt", "w") as op:
        for i in failed_ids:
            s = str(i) + "\n"
            op.write(s)
