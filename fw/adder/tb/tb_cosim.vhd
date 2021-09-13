library work;
   context work.cosim_context;
   use work.cosim.all;


entity tb_cosim is
end entity;


architecture test of tb_cosim is

   constant C_READ_FIFO_PATH  : string := "/tmp/fusesoc_cosim_example/adder_python_vhdl";
   constant C_WRITE_FIFO_PATH : string := "/tmp/fusesoc_cosim_example/adder_vhdl_python";

   signal clk : std_logic := '0';

   -- Test bench specific signals.
   signal a, b : unsigned(30 downto 0);
   signal s    : unsigned(31 downto 0);

   -- Wishbone interfaces.
   signal uvvm_wb_if : t_wishbone_if (
      dat_o(31 downto 0),
      dat_i(31 downto 0),
      adr_o(31 downto 0)
   ) := init_wishbone_if_signals(32, 32);

   signal wb_ms: t_wishbone_master_out;
   signal wb_sm: t_wishbone_slave_out;

begin

   clk <= not clk after C_CLK_PERIOD / 2;


   wb_ms.cyc <= uvvm_wb_if.cyc_o;
   wb_ms.stb <= uvvm_wb_if.stb_o;
   wb_ms.adr <= uvvm_wb_if.adr_o;
   wb_ms.sel <= (others => '0');
   wb_ms.we  <= uvvm_wb_if.we_o;
   wb_ms.dat <= uvvm_wb_if.dat_o;

   uvvm_wb_if.dat_i <= wb_sm.dat;
   uvvm_wb_if.ack_i <= wb_sm.ack;

   cosim_interface(C_READ_FIFO_PATH, C_WRITE_FIFO_PATH, clk, uvvm_wb_if, C_WB_BFM_CONFIG);


   agwb_top : entity agwb.top
   port map (
      slave_i => wb_ms,
      slave_o => wb_sm,

      a_o => a,
      b_o => b,
      s_i => s,

      rst_n_i => '1',
      clk_sys_i => clk
   );


   DUT : entity work.adder
   port map (
      clk_i => clk,
      a_i   => a,
      b_i   => b,
      s_o   => s
   );

end architecture;
