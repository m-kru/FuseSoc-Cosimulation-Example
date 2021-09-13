import random
import logging as log
log.basicConfig(
        level=log.DEBUG,
        format="%(asctime)s,%(msecs)03d:%(module)s:%(levelname)s:%(message)s",
        datefmt="%H:%M:%S",
)

import agwb
from cosim_interface import CosimInterface

WRITE_FIFO_PATH = "/tmp/fusesoc_cosim_example/adder_python_vhdl"
READ_FIFO_PATH  = "/tmp/fusesoc_cosim_example/adder_vhdl_python"

CLOCK_PERIOD_40 = 25

def delay_function():
    return CLOCK_PERIOD_40 * random.randrange(80,90)

try:
    log.info("Starting cosimulation")

    cosim_interface = CosimInterface(WRITE_FIFO_PATH, READ_FIFO_PATH, delay_function, True)
    agwb_top = agwb.top(cosim_interface, 0)

    cosim_interface.wait(10 * CLOCK_PERIOD_40)
    log.info("Ending cosimulation")
    cosim_interface.end(0)
except Exception as E:
    cosim_interface.end(1)
    log.exception(E)
