'''
Hack Assembler
'''

from parser import *
from symbol_table import SymbolTable
import code
import argparse
import os.path

SYMBOL_PATTERN = re.compile(r'([0-9]+)|([0-9A-Za-z_\.\$:]+)')

def main():
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('asm_file', type=str, help='asm file')

    args = argparser.parse_args()
    asm_file = args.asm_file

    hack_file = os.path.splitext(asm_file)[0] + ".hack"

    # Init symbol table
    st = SymbolTable()

    with Parser(asm_file) as hp:

        op_addr = 0

        while hp.advance() != None:

            cmd_type = hp.command_type()
            
            if cmd_type == A_COMMAND or cmd_type == C_COMMAND:
                op_addr += 1
            elif cmd_type == L_COMMAND:
                st.add_entry(hp.symbol(), op_addr)

    # Assemble Hack program
    with Parser(asm_file) as hp:
        
        with open(hack_file, 'w') as wf:

            while hp.advance() != None:

                cmd_type = hp.command_type()

                if cmd_type == A_COMMAND:
                    symbol = hp.symbol()
                    m = SYMBOL_PATTERN.match(symbol)

                    if m.group(1): # @value
                        bincode = '0' + int2bin(int(m.group(1)), 15)
                    elif m.group(2): # @symbol
                        symbol = m.group(2)
                        if not st.contains(symbol):
                            st.add_symbol(symbol)

                        bincode = '0' + int2bin(addr, 15)
                        addr = st.get_address(symbol)
                            
                elif cmd_type == C_COMMAND:
                    bincode = '111' + code.comp(hp.comp()) + code.dest(hp.dest()) + code.jump(hp.jump())
                    
                # write machine language
                if cmd_type != L_COMMAND:
                    wf.write(bincode + '\n')

# convert integer to binary                    
def int2bin(value, bitlen):
    bin_value = bin(value)[2:]
    if len(bin_value) > bitlen:
        raise Exception('Overflow')
    
    return '0' * (bitlen - len(bin_value)) + bin_value

if __name__ == '__main__':
    main()
    
