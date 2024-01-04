#!/usr/bin/env python
#
# SCons tool for yosys
# For more information see: https://github.com/YosysHQ/yosys

from SCons.Builder import Builder
from SCons.Scanner import Scanner
import re

def generate(env):

    verilog_include_pattern = re.compile(r"^[^\S\v]*`include\s+\"(\S+)\"", re.M)
    def scan_verilog(node, path, env):
        contents = node.get_text_contents()
        includes = v_include_pattern.findall(contents)
        return includes

    ys_source_pattern = re.compile(r"^[^\S\v]*(?:script|read\w*)(?:[^\S\v]+(?!\#)(?:-\S+|(\S+)))+", re.M)
    ys_write_pattern = re.compile(r"^[^\S\v]*write\w*(?:[^\S\v]+(?!\#)(?:-\S+|(\S+)))+", re.M)
    ys_synth_pattern = re.compile(r"^[^\S\v]*synth\w*(?:[^\S\v]+(?!\#)(?:-json\s+(\S+)|\S+))+", re.M)
    def scan_yosys_script(node, path, env):
        contents = node.get_text_contents()
        sources = ys_source_pattern.findall(contents)
        return sources

    yosys_script_scanner = Scanner(
        function = scan_yosys_script, 
        skeys = [ ".ys" ] 
    )

    def emit_yosys_script_files(target, source, env):
        contents = source[0].get_text_contents()
        sources =  ys_source_pattern.findall(contents)
        targets = ys_write_pattern.findall(contents) + ys_synth_pattern.findall(contents)
        return targets, source + sources

    yosys_script_builder = Builder(
        action = "pushd ${SOURCES.srcdir}; $YOSYS $YOSYSFLAGS -s ${SOURCE.file}; popd; cp ${SOURCE.srcdir}/${TARGET.file} $TARGET; rm ${SOURCE.srcdir}/${TARGET.file}",
        src_suffix = ".ys",
        source_scanner = yosys_script_scanner,
        emitter = emit_yosys_script_files,
    )

    env.Replace(
        YOSYS = "yosys"
    )
    
    env.Append(
        BUILDERS = {
            "YosysScript": yosys_script_builder
        },
        YOSYSFLAGS = []
    )


def exists():
    return True
