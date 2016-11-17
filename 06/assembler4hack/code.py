'''
convert mnemonic to binary for Hack-Assembly
'''

dest2bin = {
    'null' : '000',
    'M'    : '001',
    'D'    : '010',
    'MD'   : '011',
    'A'    : '100',
    'AM'   : '101',
    'AD'   : '110',
    'AMD'  : '111'
};

comp2bin = {
    '0'   : '0101010',
    '1'   : '0111111',
    '-1'  : '0111010',
    'D'   : '0001100',
    'A'   : '0110000',
    'M'   : '1110000',
    '!D'  : '0001101',
    '!A'  : '0110001',
    '!M'  : '1110001',
    '-D'  : '0001111',
    '-A'  : '0110011',
    '-M'  : '1110011',
    'D+1' : '0011111',
    'A+1' : '0110111',
    'M+1' : '1110111',
    'D-1' : '0001110',
    'A-1' : '0110010',
    'M-1' : '1110010',
    'D+A' : '0000010',
    'D+M' : '1000010',
    'D-A' : '0010011',
    'D-M' : '1010011',
    'A-D' : '0000111',
    'M-D' : '1000111',
    'D&A' : '0000000',
    'D&M' : '1000000',
    'D|A' : '0010101',
    'D|M' : '1010101'
};

jump2bin = {
    'null' : '000',
    'JGT'  : '001',
    'JEQ'  : '010',
    'JGE'  : '011',
    'JLT'  : '100',
    'JNE'  : '101',
    'JLE'  : '110',
    'JMP'  : '111'
};

def dest(mnemonic):
    '''
    convert dest mnemonic to binary
    '''
    if mnemonic == None:
        return dest2bin['null']

    elif mnemonic in dest2bin:
        return dest2bin[mnemonic]

    else:
        raise Exception('Mnemonic Convert Error: dest')

def comp(mnemonic):
    '''
    convert comp mnemonic to binary
    '''
    if mnemonic == None:
        return comp2bin['null']

    elif mnemonic in comp2bin:
        return comp2bin[mnemonic]

    else:
        raise Exception('Mnemonic Convert Error: comp')

def jump(mnemonic):
    '''
    convert jump mnemonic to binary
    '''
    if mnemonic == None:
        return jump2bin['null']

    elif mnemonic in jump2bin:
        return jump2bin[mnemonic]

    else:
        raise Exception('Mnemonic Convert Error: jump')    
    
