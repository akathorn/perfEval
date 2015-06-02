#!/usr/bin/python

import sys

conf = """DIP_DISTRIBUTED true
DIP_QUERY_NAME tpch7
DIP_QUERY_PLAN ch.epfl.data.squall.examples.imperative.shj.TPCH7Plan
DIP_TOPOLOGY_NAME_PREFIX perfeval_
#DIP_NUM_ACKERS 0

#DIP_DATA_PATH /shared/tpch/0.01G/
DIP_DATA_PATH /data/squall_blade/data/tpchdb/1G

#DIP_NUM_WORKERS 8

NATION1_PAR 1
NATION2_PAR 1
CUSTOMER_PAR 1
ORDERS_PAR 1
SUPPLIER_PAR 1
LINEITEM_PAR 1

NATION2_CUSTOMER_PAR 1
NATION2_CUSTOMER_ORDERS_PAR 1
SUPPLIER_NATION1_PAR 1
LINEITEM_SUPPLIER_NATION1_PAR 1
NATION2_CUSTOMER_ORDERS_LINEITEM_SUPPLIER_NATION1_PAR 1

########################################################################
#   possible values are MANUAL_BATCH
# BATCH_SEND_MODE MANUAL_BATCH
# BATCH_SIZE %s

CUSTOM_TIMESTAMP true
#   ignoring latencies in 1st second, they are 3 orders of magnitudes bigger
INIT_IGNORED_TUPLES 0

#   compute latency for every FREQ_TUPLE_LOG_COMPUTEth tuple on the last component (does not depend on BATCH_SEND_MODE)
FREQ_TUPLE_LOG_COMPUTE 1
#   write average latency for every FREQ_TUPLE_LOG_WRITEth batch on the last component
#   FREQ_TUPLE_LOG_WRITE has to be divisible with FREQ_TUPLE_LOG_COMPUTE
FREQ_TUPLE_LOG_WRITE 100
########################################################################

#below are unlikely to change
DIP_EXTENSION .tbl
DIP_READ_SPLIT_DELIMITER \|
DIP_GLOBAL_ADD_DELIMITER |
DIP_GLOBAL_SPLIT_DELIMITER \|

DIP_KILL_AT_THE_END true
# Storage manager parameters
# Storage directory for local runs
STORAGE_LOCAL_DIR /tmp/ramdisk
# Storage directory for cluster runs
STORAGE_CLUSTER_DIR /data/squall_zone/storage
STORAGE_COLD_START true
STORAGE_MEMORY_SIZE_MB 4096"""


conf = { words[0]: words[1] for words in
         [ line.split() for line in conf.split("\n")
                        if line.strip() and line[0] != "#"] }

def generate(out, extra_conf):
    print "Writing to", out, "with additional configuration", extra_conf

    outconf = conf.copy()
    outconf.update(extra_conf)

    write_conf(outconf, out)

def write_conf(conf, out):
    f = open(out, "w")
    f.write("\n".join([ k + " " + v for (k,v) in conf.iteritems() ]))
    f.flush()
    f.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please specify the output file"
        sys.exit(1)

    extra_conf = {}
    for kv in map(lambda x: x.split("="), sys.argv):
        if len(kv) == 2:
            extra_conf[kv[0]] = kv[1]

    generate(sys.argv[1], extra_conf)


    #for batchsize in [ 10 ** n for n in range(5) ]:
        #conf += "\nstorm.messaging.netty.transfer.batch.size 1"
        # BATCH_SEND_MODE MANUAL_BATCH
        # BATCH_SIZE %s
