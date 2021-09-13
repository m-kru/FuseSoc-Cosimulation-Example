import os
import logging as log

class CosimInterface:
    def __init__(self, write_fifo_path, read_fifo_path, delay_function=None, delay=False):
        self.write_fifo_path = write_fifo_path
        self.read_fifo_path = read_fifo_path

        self._make_fifos()
        self.write_fifo = open(write_fifo_path, "w")
        self.read_fifo = open(read_fifo_path, "r")

        if delay and delay_function is None:
            raise Exception("delay set to 'True', but delay_function not provided")

        self.delay_function = delay_function
        self.delay = delay

    def _make_fifos(self):
        self._remove_fifos()
        log.info("Making FIFOs")
        os.mkfifo(self.write_fifo_path)
        os.mkfifo(self.read_fifo_path)

    def _remove_fifos(self):
        try:
            log.info("Removing FIFOs")
            os.remove(self.write_fifo_path)
            os.remove(self.read_fifo_path)
        except:
            pass

    def write(self, addr, val):
        if self.delay:
            self.wait(self.delay_function())

        log.info("Writng address 0x%.8x, value %d (0x%.8x) (%s)" % (addr, val, val, bin(val)))

        cmd = "W" + ("%.8x" % addr) + "," + ("%.8x" % val) + "\n"
        self.write_fifo.write(cmd)
        self.write_fifo.flush()

        s = self.read_fifo.readline()
        if s.strip() == "ACK":
            return
        else:
            raise Exception("Wrong status returned:" + s.strip())

    def read(self, addr):
        if self.delay:
            self.wait(self.delay_function())

        log.info("Reading address 0x%.8x" % addr)

        cmd = "R" + ("%.8x" % addr) + "\n"
        self.write_fifo.write(cmd)
        self.write_fifo.flush()

        s = self.read_fifo.readline()
        if s.strip() == "ERR":
           raise Exception("Error status returned")

        val = int(s, 2)
        log.info("Read value %d (0x%.8x) (%s)" % (val, val, bin(val)))

        return val

    def wait(self, time_ns):
        assert time_ns > 0 , "Wait time must be greater than 0"

        log.info("Waiting for %d ns" % time_ns)

        cmd = "T" + ("%.8x" % time_ns) + "\n"
        self.write_fifo.write(cmd)
        self.write_fifo.flush()

        s = self.read_fifo.readline()
        if s.strip() == "ACK":
            return
        else:
            raise Exception("Wrong status returned:" + s.strip())

    def end(self, status):
        log.info("Ending with status %d" % status)

        cmd = "E" + ("%.8x" % status) + "\n"
        self.write_fifo.write(cmd)
        self.write_fifo.flush()

        s = self.read_fifo.readline()
        if s.strip() == "ACK":
            self._remove_fifos()
            return
        else:
            raise Exception("Wrong status returned:" + s.strip())
