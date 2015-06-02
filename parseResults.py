#!/usr/bin/python

import os, json, datetime

RESULT_PATH = "./results"

def get_uptimes(log):
    uptimes = {}
    for line in log:
        if "uptime:" in line:
            component = line.split()[0].split(":")[1][:-1]
            uptime = int(line.split("uptime:")[1])
            uptimes[component] = uptime
    return uptimes

def get_configuration(log):
    s = "".join(log)
    return json.loads(s[s.find('{'):s.find('}')+1])

def read_log(logfile):
    logfile = open(RESULT_PATH + "/" + logfile)
    log = logfile.readlines()
    logfile.close()
    return map(lambda l: l.strip(), log)

def main():
    results = []
    for logfile in os.listdir(RESULT_PATH):
        log = read_log(logfile)
        uptime = sorted(get_uptimes(log).values())
        configuration = get_configuration(log)
        timestamp = int(logfile.split("-")[-1])
        results.append((int(configuration["BATCH_SIZE"]), uptime, timestamp))
    results.sort()
    for (batchsize, uptime, timestamp) in results:
        print datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M"),
        print " ", batchsize, "\t", max(uptime), "\t", uptime


if __name__ == "__main__":
    main()
