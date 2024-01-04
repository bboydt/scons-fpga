# scons-fpga
A SCons tool for building ECP5 bitstreams.

## How to use

1) Add `yosys.py`, `nextpnr.py`, and `trellis.py` to your SCons tools (i.e. `site_scons/site_tools/`)

2) Include the tools in your environment and configure flags. See the tool files for construction variable names.
```python
env = Environment(tools = ['yosys', 'nextpnr.py', 'trellis.py', ...], ...)
```

3) Build a bitstream!
```python
ast = env.YosysScript("synth_soc.ys")
textcfg = env.Ecp5Pnr(ast)
bitstream = env.Ecp5Bitstream(textcfg)
```

## Note on Yosys Tool
I'm not very happy with how this works atm. It will likely change.
