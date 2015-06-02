#!/usr/bin/python

from generate_confs import generate


if __name__ == "__main__":
    generate("confs/no_batching", {})
    generate("confs/no_batching_no_netty", {"storm.messaging.netty.transfer.batch.size": "1"})
    for batchsize in [ 10 ** n for n in range(5) ]:
        extra_conf = {}
        extra_conf["BATCH_SEND_MODE"] = "MANUAL_BATCH"
        extra_conf["BATCH_SIZE"] = str(batchsize)
        generate("confs/%s_batching" % batchsize, extra_conf)

        extra_conf["storm.messaging.netty.transfer.batch.size"] = "1"
        generate("confs/%s_batching_no_netty" % batchsize, extra_conf)
