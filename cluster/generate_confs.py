#!/usr/bin/python


def generate_conf(batch_size):
    conf = """DIP_DISTRIBUTED true
DIP_QUERY_NAME tpch3
DIP_QUERY_PLAN ch.epfl.data.squall.examples.imperative.theta.ThetaInputDominatedPlan
DIP_TOPOLOGY_NAME_PREFIX perfeval_%s_

DIP_NUM_ACKERS 0

#InputDominated query
#JOIN TYPE 0 for Static, 1 for Naively Dynamic, 2 for Advised Dynamic, & 3 for Epochs
DIP_JOIN_TYPE 1

ORDERS_PAR 2
LINEITEM_PAR 2
LINEITEM_ORDERS_PAR 4
LINEITEM_ORDERS_RESHUF_PAR 2

#0 for heuristics and 1 for theoretical
ADVISOR_TYPE 1
EPSILON 0.1


NATION_CARD 50
CUSTOMER_CARD 50
SUPPLIER_CARD 50
ORDERS_CARD 50
LINEITEM_CARD 50

LINEITEM_ORDERS_CARD 50

DIP_THETA_CLOCK_REFRESH_RATE_MILLISECONDS 100
DIP_INPUT_FREQ_PRINT 5000
DIP_OUTPUT_FREQ_PRINT 500

########################################################################
#   possible values are MANUAL_BATCH
# BATCH_SEND_MODE MANUAL_BATCH
BATCH_SIZE %s

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
STORAGE_MEMORY_SIZE_MB 4096""" % (batch_size, batch_size)
    return conf

if __name__ == "__main__":
    for batchsize in [ 10 ** n for n in range(5) ]:
        conf = generate_conf(batchsize)
        f = open("./conf_%s" % batchsize, "w")
        f.write(conf)
        f.close()