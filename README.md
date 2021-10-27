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

## How to run?

Simply execute `fsva ::adder tb_cosim` in a shell.
The HDL output goes to the stdout.
The software output goes to the `/tmp/fusesoc_cosim_example/adder.log`.
If you want to see the software output live, simply run `tail -f /tmp/fusesoc_cosim_example/adder.log`.

## Comment

At first, when you look at the number of files, you might think that a lot of files are needed to run a single co-simulation.
But do not get mislead.
You need most of these files in any serious project anyway.
This includes bus infrastructure files (`general-cores`) and a tool for registers generation (`agwb`).
There are also some co-simulation files that are reused, so you need only one instance of them.
This includes `tb_cosim.sh`, `sw/cosim_interface.py` `fw/cosim/*`.
In the end, the only single co-simulation related files are `fw/adder/tb/tb_cosim.vhd`, and `fw/adder/tb/tb_cosim.py`.

## Further reading

[arXiv - Easy and structured approach for software and firmware co-simulation for bus centric designs](https://arxiv.org/abs/2110.10447)
