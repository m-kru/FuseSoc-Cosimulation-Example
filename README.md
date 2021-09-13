# FuseSoc Cosimulation Example

An example showing how to run software and firmware cosimulation using FuseSoc hooks.

It uses Python for the software side and VHDL (GHDL simulator) for the firmware side.
However, languages or simulator can be easily changed and the concept remains the same.

The assumption is that UVVM library is already installed.

## Directory structure

- sw - python cosimulation interface module.
- fw - directory for HDL codes and software test bench script.
- general-cores - part of the general-cores library needed to make the Wishbone infrastructure work.
