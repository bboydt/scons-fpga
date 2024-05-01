# SCons tool for sv2v
#

from SCons.Action import Action
from SCons.Builder import Builder

sv2v_builder = None
sv2v_action = None

def generate(env):

    # Create actions and builders
    #

    global sv2v_builder
    if (sv2v_builder is None):
        sv2v_builder = Builder(action = {},
                               prefix = '$SVPREFIX',
                               suffix = '$SVSUFFIX',
                               emitter = {},
                               source_ext_match = None,
                               single_source = False)

    global sv2v_action
    if (sv2v_action is None):
        sv2v_action = Action('$SV2VCOM', '$SV2VCOMSTR')

    # Prep environment
    #

    if ('VERILOGPREFIX' not in env):
        env['VERILOGPREFIX'] = '';
    if ('VERILOGSUFFIX' not in env):
        env['VERILOGSUFFIX'] = '.v';

    if ('SVPREFIX' not in env):
        env['SVPREFIX'] = '';
    if ('SVSUFFIX' not in env):
        env['SVSUFFIX'] = '.sv';

    env['SV2V'] = 'sv2v'
    env['SV2VFLAGS'] = ''

    env["SV2VINCPREFIX"] = "-I"
    env["SV2VINCSUFFIX"] = ""
    env["_SV2VINCFLAGS"] = "$( ${_concat(SV2VINCPREFIX, VPATH, SV2VINCSUFFIX, __env__, RDirs)} $)"

    env["SV2VDEFPREFIX"] = "-D"
    env["SV2VDEFSUFFIX"] = ""
    env["_SV2VDEFFLAGS"] = "$( ${_defines(SV2VDEFPREFIX, VDEFINES, SV2VDEFSUFFIX, __env__)} $)"

    env['SV2VCOM'] = '$SV2V $SV2VFLAGS $_SV2VINCFLAGS $_SV2VDEFFLAGS -w=$TARGET $SOURCES'

    # Add builders
    #

    sv2v_builder.add_action('$SVSUFFIX', sv2v_action)

    env['BUILDERS']['Verilog'] = sv2v_builder

def exists():
    return True
