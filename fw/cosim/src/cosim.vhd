library ieee;
   use ieee.std_logic_1164.all;
   use ieee.numeric_std.all;

library std;
  use std.textio.all;

library general_cores;
   use general_cores.wishbone_pkg.all;

library uvvm_util;
   context uvvm_util.uvvm_util_context;

library bitvis_vip_wishbone;
   use bitvis_vip_wishbone.wishbone_bfm_pkg.all;


package cosim is

   constant C_CLK_PERIOD : time := 25 ns;

   constant C_WB_BFM_CONFIG : t_wishbone_bfm_config := (
      max_wait_cycles          => 10,
      max_wait_cycles_severity => failure,
      clock_period             => C_CLK_PERIOD,
      clock_period_margin      => 0 ns,
      clock_margin_severity    => TB_ERROR,
      setup_time               => 2.5 ns,
      hold_time                => 2.5 ns,
      id_for_bfm               => ID_BFM,
      id_for_bfm_wait          => ID_BFM_WAIT,
      id_for_bfm_poll          => ID_BFM_POLL
   );


   procedure uvvm_to_gc_wishbone_adapter (
      signal uvvm_wb_if : inout t_wishbone_if;
      signal gc_wb_ms   : inout t_wishbone_master_out;
      signal gc_wb_sm   : inout t_wishbone_master_in
   );


   procedure cosim_interface (
      constant read_fifo_path : string;
      constant write_fifo_path : string;
      signal wb_clk : in std_logic;
      signal uvvm_wb_if : inout t_wishbone_if;
      constant wb_bfm_config : t_wishbone_bfm_config
   );

end package;


package body cosim is

   procedure uvvm_to_gc_wishbone_adapter (
      signal uvvm_wb_if : inout t_wishbone_if;
      signal gc_wb_ms   : inout t_wishbone_master_out;
      signal gc_wb_sm   : inout t_wishbone_master_in
   ) is
   begin
      -- General Cores WB <= UVVM WB
      gc_wb_ms.cyc <= uvvm_wb_if.cyc_o;
      gc_wb_ms.stb <= uvvm_wb_if.stb_o;
      gc_wb_ms.adr <= uvvm_wb_if.adr_o;
      gc_wb_ms.sel <= (others => '0');
      gc_wb_ms.we  <= uvvm_wb_if.we_o;
      gc_wb_ms.dat <= uvvm_wb_if.dat_o;

      -- UVVM WB <= General Cores WB
      uvvm_wb_if.dat_i <= gc_wb_sm.dat;
      uvvm_wb_if.ack_i <= gc_wb_sm.ack;
   end procedure;


   procedure cosim_interface (
      constant read_fifo_path : string;
      constant write_fifo_path : string;
      signal wb_clk : in std_logic;
      signal uvvm_wb_if : inout t_wishbone_if;
      constant wb_bfm_config : t_wishbone_bfm_config
   ) is
      file wr_pipe  : text;
      file rd_pipe   : text;

      variable code    : character;
      variable rd_line : line;
      variable wr_line : line;

      variable addr : unsigned(31 downto 0);
      variable val  : std_logic_vector(31 downto 0);

      variable end_status : integer;
   begin
      file_open(rd_pipe, read_fifo_path, read_mode);
      file_open(wr_pipe, write_fifo_path, write_mode);

      while not endfile(rd_pipe) loop
         readline(rd_pipe, rd_line);
         read(rd_line, code);

         case code is
            when 'W' =>
               hread(rd_line, addr);
               read(rd_line, code);
               if code /= ',' then
                  error("Error: wrong separator in the write command");
               end if;
               hread(rd_line, val);

               wishbone_write(addr, val, "cosim interface", wb_clk, uvvm_wb_if, config => wb_bfm_config);

               write(wr_line, string'("ACK"));
               writeline(wr_pipe, wr_line);
               flush(wr_pipe);
            when 'R' =>
               hread(rd_line, addr);

               wishbone_read(addr, val, "cosim interface", wb_clk, uvvm_wb_if, config => wb_bfm_config);

               write(wr_line, to_string(val));
               writeline(wr_pipe, wr_line);
               flush(wr_pipe);
            when 'T' =>
               hread(rd_line, val);

               wait for to_integer(unsigned(val)) * 1 ns;

               write(wr_line, string'("ACK"));
               writeline(wr_pipe, wr_line);
               flush(wr_pipe);
            when 'E' =>
               read(rd_line, end_status);

               write(wr_line, string'("ACK"));
               writeline(wr_pipe, wr_line);
               flush(wr_pipe);

               if end_status /= 0 then
                  failure("End status " & integer'image(end_status) & ", check Python log: /tmp/tb_cosim_rcv_frames_shuffler.log");
               end if;

               file_close(rd_pipe);
               file_close(wr_pipe);
               std.env.finish;
            when others =>
               failure("Cosim Interface - unknown command: '" & code & "'");
         end case;
      end loop;
   end procedure;

end package body;
