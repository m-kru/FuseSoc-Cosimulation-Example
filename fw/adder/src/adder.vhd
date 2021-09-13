library ieee;
   use ieee.std_logic_1164.all;
   use ieee.numeric_std.all;


entity adder is
   port(
      clk_i : in  std_logic;
      a_i   : in  unsigned(30 downto 0);
      b_i   : in  unsigned(30 downto 0);
      s_o   : out unsigned(31 downto 0)
   );
end entity;


architecture rtl of adder is
begin

   process (clk_i) is
   begin
      if rising_edge(clk_i) then
         s_o <= resize(a_i, s_o'length) + resize(b_i, s_o'length);
      end if;
   end process;

end architecture;
