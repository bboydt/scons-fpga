#!/usr/bin/env python
#
# SCons tool for nextpnr
# For more information see: https://github.com/YosysHQ/nextpnr

from SCons.Builder import Builder

def generate(env):

    ecp5_pnr_builder = Builder(
        action = "$NEXTPNR-ecp5 $PNRFLAGS --json $SOURCE --textcfg $TARGET",
        suffix = ".config",
        src_suffix = ".json",
        src_builder = "YosysScript",
        single_source = True
    )

    # TODO generic gowin ice40 machxo2 nexus

    env.Replace(
        NEXTPNR = "nextpnr"
    )
    
    env.Append(
        BUILDERS = {
            "Ecp5Pnr": ecp5_pnr_builder
        },
        PNRFLAGS = []
    )

def exists():
    return True
