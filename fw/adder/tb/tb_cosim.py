import random
import logging as log
log.basicConfig(
        level=log.DEBUG,
        format="%(module)s:%(levelname)s:%(message)s",
        datefmt="%H:%M:%S",
)

import agwb
from cosim_interface import CosimInterface

WRITE_FIFO_PATH = "/tmp/fusesoc_cosim_example/adder_python_vhdl"
READ_FIFO_PATH  = "/tmp/fusesoc_cosim_example/adder_vhdl_python"

CLOCK_PERIOD_40 = 25

def delay_function():
    return CLOCK_PERIOD_40 * random.randrange(10,40)

try:
    log.info("Starting adder cosimulation")

    cosim_interface = CosimInterface(WRITE_FIFO_PATH, READ_FIFO_PATH, delay_function, True)

    agwb_top = agwb.top(cosim_interface, 0)

    log.info("Generating random numbers")
    a = random.randint(0, 2**31 - 1)
    b = random.randint(0, 2**31 - 1)
    log.info("a = {}, b = {}".format(a, b))
    s = a + b
    log.info("Expected sum = {}".format(s))

    agwb_top.a.write(a)
    agwb_top.b.write(b)

    if s != agwb_top.s.read():
        log.error("Read wrong value")

    log.info("Read correct value")

    cosim_interface.wait(10 * CLOCK_PERIOD_40)
    log.info("Ending cosimulation")
    cosim_interface.end(0)
except Exception as E:
    cosim_interface.end(1)
    log.exception(E)
