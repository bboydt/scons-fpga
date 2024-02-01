# scons-fpga 👾
A collection of SCons tools for building bitstreams and testing designs.

## Tools
You can specific tools with the following names:
- `yosys` provides https://github.com/YosysHQ/yosys
- `nextpnr` provides https://github.com/YosysHQ/nextpnr
- `trellis` provides https://github.com/YosysHQ/prjtrellis
- `icarus` provides https://github.com/steveicarus/iverilog

## How to use

1) For each tool you want add `<tool>.py` into your SCons tools (i.e. `site_scons/site_tools/`).<br>or<br>Add this repo as a submodule to your repo and add its path to `toolpath` in your environment.
2) Include the tools in your environment and configure flags. See the tool files for construction variable names.
```python
env = Environment(tools = ['yosys', 'nextpnr.py', 'trellis.py', 'icarus', ...], ...)
```

3) Build a bitstream!
```python
ast = env.YosysScript("synth_soc.ys")
textcfg = env.Ecp5Pnr(ast)
bitstream = env.Ecp5Bitstream(textcfg)
```

## Note on Yosys Tool
I'm not very happy with how this works atm. It will likely change.
