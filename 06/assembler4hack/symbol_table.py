'''
symbol table for Hack-Assembly
'''

class SymbolTable():
    '''
    symbol table for Hack-Assembly
    '''

    def __init__(self):
        self.symbol_table = {
            'SP'    : 0,
            'LCL'   : 1,
            'ARG'   : 2,
            'THIS'  : 3,
            'THAT'  : 4,
            'R0'    : 0,
            'R1'    : 1,
            'R2'    : 2,
            'R3'    : 3,
            'R4'    : 4,
            'R5'    : 5,
            'R6'    : 6,
            'R7'    : 7,
            'R8'    : 8,
            'R9'    : 9,
            'R10'   : 10,
            'R11'   : 11,
            'R12'   : 12,
            'R13'   : 13,
            'R14'   : 14,
            'R15'   : 15,
            'SCREEN': 16384,
            'KBD'   : 24576
        }        
        self.next_addr = 16

    def add_entry(self, symbol, address):
        '''
        add (symbol, address) pair to symbol table
        '''
        self.symbol_table[symbol] = address

    def add_symbol(self, symbol):
        '''
        add symbol to symbol table
        '''
        if not self.contains(symbol):
            self.add_entry(symbol, self.next_addr)
            self.next_addr += 1
        
    def contains(self, symbol):
        '''
        check symbol is in symbol_table
        '''
        if symbol in self.symbol_table:
            return True
        else:
            return False
        
    def get_address(self, symbol):
        '''
        notice address of symbol
        '''
        if self.contains(symbol):
            return self.symbol_table[symbol]
        else:
            raise Exception('Symbol does not exist.')
        
