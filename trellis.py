#!/usr/bin/env python
#
# SCons tool for project trellis
# For more information see: https://github.com/YosysHQ/prjtrellis

from SCons.Builder import Builder

def generate(env):

    ecp5_bitstream_builder = Builder(
        action = '$ECPPACK $ECPPACKFLAGS --input $SOURCE --bit $TARGET',
        suffix = '.bit',
        src_suffix = '.config',
        src_builder = 'Ecp5Pnr',
        single_source = True
    )

    # TODO ecpbram ecpdap ecperf ecpmulti ecppack ecppll ecpprog ecpunpack

    env.Replace(
        ECPBRAM = 'ecpbram',
        ECPDAP = 'ecpdap',
        ECPERF = 'ecperf',
        ECPMULTI = 'ecpmulti',
        ECPPACK = 'ecppack',
        ECPPLL = 'ecppll',
        ECPPROG = 'ecpprog',
        ECPUNPACK = 'ecpunpack',
    )
    
    env.Append(
        BUILDERS = {
            'Ecp5Bitstream': ecp5_bitstream_builder
        },
        ECPPACKFLAGS = []
    )

def exists():
    return True

