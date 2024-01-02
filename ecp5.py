#
# ECP5 Gateware Synthesis
#

import re

import SCons.Action
import SCons.Builder
import SCons.Defaults
import SCons.Scanner.D
import SCons.Tool

# actions
#

synthesize = SCons.Action.Action(
    "$YOSYS $YOSYS_FLAGS -p \"read_verilog $SOURCES; synth_ecp5 -json $TARGET\"",
    "$YOSYSCOMSTR"
)

place_and_route = SCons.Action.Action(
    "$NEXTPNR $NEXTPNR_FLAGS --json $SOURCE --textcfg $TARGET",
    "$NEXTPNRCOMSTR"
)

pack_bitstream = SCons.Action.Action(
    "$ECPPACK $ECPPACK_FLAGS --input $SOURCE --bit $TARGET",
    "$ECPPACKCOMSTR"
)

# emitter functions
#

def emit_text_config_files_verilog(target, source, env):
    synthesis = env.Synthesis(source)
    return target, [synthesis]

def emit_bitstream_files_verilog(target, source, env):
    synthesis = env.Synthesis(source)
    text_config = env.TextConfig(synthesis)
    return target, [text_config]

def emit_bitstream_files_json(target, source, env):
    text_config = env.TextConfig(source)
    return target, [text_config]

# builders
#

synthesis_builder = SCons.Builder.Builder(
    action = synthesize,
    src_suffix = ".v",
    suffix = ".json",
    emitter = {}
)

text_config_builder = SCons.Builder.Builder(
    action = place_and_route,
    suffix = ".config",
    emitter = {
        ".v": emit_text_config_files_verilog,
        ".json": None,
    },
)

bitstream_builder = SCons.Builder.Builder(
    action = pack_bitstream,
    suffix = ".bit",
    emitter = {
        ".v": emit_bitstream_files_verilog,
        ".json": emit_bitstream_files_json,
        ".config": None
    },
)

# verilog dependency scanner
#

include_re = re.compile(r"^`include\s+\"(\S+)\"$", re.M)
      
def verilog_scan(node, env, path):
    contents = node.get_text_contents()
    return [node.srcnode().dir.File(x) for x in include_re.findall(contents)]

verilog_scanner = SCons.Scanner.Scanner(function = verilog_scan, skeys = ['.v'])

def generate(env) -> None:
    env["BUILDERS"]["Synthesis"] = synthesis_builder
    env["BUILDERS"]["TextConfig"] = text_config_builder
    env["BUILDERS"]["Bitstream"] = bitstream_builder

    env["SCANNERS"] = verilog_scanner

    env["YOSYS"] = "yosys"
    env["NEXTPNR"] = "nextpnr-ecp5"
    env["ECPPACK"] = "ecppack"

    env["YOSYSCOMSTR"] = "yosys $TARGET"
    env["NEXTPNRCOMSTR"] = "nextpnr-ecp5 $TARGET"
    env["ECPPACKCOMSTR"] = "ecppack $TARGET"

    env["YOSYS_FLAGS"] = ""
    env["NEXTPNR_FLAGS"] = ""
    env["ECPPACK_FLAGS"] = ""

def exists(env):
    return env.Detect('YOSYS')

