# FuseSoc Cosimulation Example

An example showing how to run software and firmware cosimulation using FuseSoc hooks.

It uses Python for the software side and VHDL ([GHDL](https://github.com/ghdl/ghdl) simulator) for the firmware side.
However, languages or simulator can be easily changed and the concept remains the same.

## Dependencies

The following components are assumed to be installed:

- [GHDL](https://github.com/ghdl/ghdl) simulator,
- [UVVM](https://github.com/UVVM/UVVM) library,
- [FuseSoc](https://github.com/olofk/fusesoc),
- [fsva](https://github.com/m-kru/fsva).

## Directory structure

- [agwb](https://github.com/wzab/agwb) - tool for generating registers.
- sw - python cosimulation interface module.
- fw - directory for HDL codes and software test bench script.
- general-cores - part of the general-cores library needed to make the Wishbone infrastructure work.
