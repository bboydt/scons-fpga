# SCons tool for Icarus Verilog
#
# Builders
# - VVPFile: builds a vvp file that can be run with vvp

from SCons.Builder import Builder
from SCons.Action import Action

vvp_builder = None
vvp_action = None

def generate(env):

    # Create actions and builders
    #

    global vvp_builder
    if (vvp_builder is None):
        vvp_builder = Builder(action = {},
                              prefix = "$VVPPREFIX",
                              suffix = "$VVPSUFFIX",
                              emitter = {},
                              source_ext_match = None,
                              single_source = False)

    global vvp_action
    if (vvp_action is None):
        vvp_action = Action("$VVPCOM", "$VVPCOMSTR")

    # Prep environment
    #

    if ("VERILOGPREFIX" not in env):
        env["VERILOGPREFIX"] = ""

    if ("VERILOGSUFFIX" not in env):
        env["VERILOGSUFFIX"] = ".v"

    env["VPPPREFIX"] = ""
    env["VPPSUFFIX"] = ".vvp"

    env["IV"] = "iverilog"
    env["IVFLAGS"] = ""
        
    env["IVINCPREFIX"] = "-I"
    env["IVINCSUFFIX"] = ""
    env["_VINCFLAGS"] = "$( ${_concat(IVINCPREFIX, VPATH, IVINCSUFFIX, __env__, RDirs)} $)"

    env["IVDEFPREFIX"] = "-D"
    env["IVDEFSUFFIX"] = ""
    env["_VDEFFLAGS"] = "$( ${_defines(IVDEFPREFIX, VDEFINES, IVDEFSUFFIX, __env__)} $)"

    env["IVPRMPREFIX"] = "-P"
    env["IVPRMSUFFIX"] = ""
    env["_VPRMFLAGS"] = "$( ${_defines(IVPRMPREFIX, VPARAMS, IVPRMSUFFIX, __env__)} $)"

    env["VVPCOM"] = "$IV $IVFLAGS $_VINCFLAGS $_VDEFFLAGS $_VPRMFLAGS -o $TARGET $SOURCES"

    # Add builders
    #

    vvp_builder.add_action(".v", vvp_action)

    env["BUILDERS"]["VVPFile"] = vvp_builder

def exists():
    return True
