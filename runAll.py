#!/usr/bin/python

import os, time, random
from subprocess import *

STORM_SCRIPT = "/home/akathorn/Squall/apache-storm-0.9.4/bin/storm"
SQUALL_JAR = "squall/squall-core/target/squall-standalone-0.2.0.jar"
CONF_DIR   = "perfEval/nonetty"
RUNS = 5

def call_storm(conf):
    return check_call(STORM_SCRIPT + " jar "+ SQUALL_JAR +" ch.epfl.data.squall.main.Main %s" % conf, shell=True)

def wait_topology():
    print "Waiting for storm to be free"
    stop = False
    while True:
        storm_list = check_output(STORM_SCRIPT + " list", shell=True)
        last_line  = storm_list.strip().split("\n")[-1]
        print "\t" + last_line.strip()
        if last_line == "No topologies running.":
            break
        # else:
        #     all_status = get_all_status(storm_list)
        #     if all([x == "KILLED" for x in all_status]):
        #         break

        time.sleep(5)

def get_all_status(lines):
    lines = lines.strip().split("\n")
    while lines[0] != "-" * 67:
        lines.pop(0)
    lines.pop(0)
    return [line.strip().split()[1] for line in lines]

if __name__ == "__main__":
    confs = os.listdir(CONF_DIR) * RUNS
    random.shuffle(confs)
    for conf in confs:
        wait_topology()
        print "Running configuration " + conf
        call_storm(CONF_DIR + "/" + conf)

