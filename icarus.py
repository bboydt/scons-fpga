# SCons tool for Icarus Verilog
#
# Builders
# - VVPFile: builds a vvp file that can be run with vvp
#
# Methods:
# - VVPRun: adds an action that run for a given vvp file

from SCons.Builder import Builder
from SCons.Action import Action

vvp_file_builder = None
vvp_file_action = None
vvp_run_action = None

def vvp_run_method(self, target):
    self.AddPostAction(target, vvp_run_action)

def generate(env):

    # Create actions and builders
    #

    global vvp_file_builder
    if (vvp_file_builder is None):
        vvp_file_builder = Builder(action = {},
                              prefix = "$VVPPREFIX",
                              suffix = "$VVPSUFFIX",
                              emitter = {},
                              source_ext_match = None,
                              single_source = False)

    global vvp_file_action
    if (vvp_file_action is None):
        vvp_file_action = Action("$VVPCOM", "$VVPCOMSTR")

    global vvp_run_action
    if (vvp_run_action is None):
        vvp_run_action = Action("$VVPRUNCOM", "$VVPRUNCOMSTR")

    # Prep environment
    #

    if ("VERILOGPREFIX" not in env):
        env["VERILOGPREFIX"] = "";
    if ("VERILOGSUFFIX" not in env):
        env["VERILOGSUFFIX"] = "";

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

    env["VVP"] = "vvp"
    env["VVPFLAS"] = ""
    env["VVPRUNCOM"] = "$VVP $VVPFLAGS $TARGET"

    # Add builders
    #

    vvp_file_builder.add_action(".v", vvp_file_action)

    env["BUILDERS"]["VVPFile"] = vvp_file_builder

    env.AddMethod(vvp_run_method, "VVPRun")

def exists():
    return True
