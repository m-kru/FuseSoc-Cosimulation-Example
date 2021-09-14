import os
import logging as log


class CosimInterface:
    def __init__(
        self, write_fifo_path, read_fifo_path, delay_function=None, delay=False
    ):
        """Create co-simulation interface.
        Parameters:
        -----------
        write_fifo_path
            Path to software -> firmware named pipe.
        read_fifo_path
            Path to firmware -> software named pipe.
        delay_function
            Reference to function returning random value when delay is set to 'True'.
        delay
            If set to 'True' there is a random delay between any write or read operation.
            Useful for modelling real access times.
        """
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
        """Create named pipes needed for inter-process communication."""
        self._remove_fifos()
        log.info("Making FIFOs")
        os.mkfifo(self.write_fifo_path)
        os.mkfifo(self.read_fifo_path)

    def _remove_fifos(self):
        """Remove named pipes."""
        try:
            log.info("Removing FIFOs")
            os.remove(self.write_fifo_path)
            os.remove(self.read_fifo_path)
        except:
            pass

    def write(self, addr, val):
        """Write register.
        Parameters
        ----------
        addr
            Register address.
        val
            Value to be written.
        """
        if self.delay:
            self.wait(self.delay_function())

        log.info(
            "Writng address 0x%.8x, value %d (0x%.8x) (%s)" % (addr, val, val, bin(val))
        )

        cmd = "W" + ("%.8x" % addr) + "," + ("%.8x" % val) + "\n"
        self.write_fifo.write(cmd)
        self.write_fifo.flush()

        s = self.read_fifo.readline()
        if s.strip() == "ACK":
            return
        else:
            raise Exception("Wrong status returned:" + s.strip())

    def read(self, addr):
        """Read register.

        Parameters
        ----------
        addr
            Register address.
        """
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
        """Wait in the simulator for a given amount of time.
        Parameters
        ----------
        time_ns
            Time to wait in nanoseconds.
        """
        assert time_ns > 0, "Wait time must be greater than 0"

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
        """End a co-simulation with a given status.
        Parameters:
        -----------
        status
            Status to be returned by the simulation process.
        """
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
