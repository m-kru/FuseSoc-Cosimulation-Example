context cosim_context is
   library ieee;
      use ieee.std_logic_1164.all;
      use ieee.numeric_std.all;

   library agwb;
      use agwb.top_pkg.all;
      use agwb.top_const_pkg.all;

   library general_cores;
      use general_cores.wishbone_pkg.all;

   library uvvm_util;
      context uvvm_util.uvvm_util_context;

   library bitvis_vip_wishbone;
      use bitvis_vip_wishbone.wishbone_bfm_pkg.all;
end context;
