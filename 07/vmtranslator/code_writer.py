'''
Translate VM into Hack
'''

from constants import *

class CodeWriter():
    '''
    Translate VM into Hack
    '''
    def __init__(self, filename):
        self.fout = open(filename, 'w')
        self.label_num = 0

    def __enter__(self):
        return self
    
    def __exit__(self, exp_type, exp_value, traceback):
        self.fout.close();

    def set_translating_file_name(self, filename):
        self.trans_file = filename
    
    def write_arithmetic(self, command):
        '''
        translate arithmetic command.
        '''
        if command in ['neg', 'not']:
            self.unary_func(command)
        
        elif command in ['add', 'sub', 'and', 'or']:
            self.binary_func(command)
            
        elif command in ['eq', 'gt', 'lt']:
            self.binary_comp(command)
        
        else:
            raise Exception('Received not existing arthmetic command.')

    def unary_func(self, command):
        self.write_codes([
            '@SP',
            'A=M-1'
        ])
        if command == 'neg':
            self.write_code('M=-M')
        elif command == 'not':
            self.write_code('M=!M')
        else:
            raise Exception('incorrect command was received.')

    def binary_func(self, command):
        self.pop2memory()
        self.write_code('D=M')
        self.pop2memory()
        if command == 'add':
            self.write_code('D=D+M')
        elif command == 'sub':
            self.write_code('D=M-D')
        elif command == 'and':
            self.write_code('D=D&M')
        elif command == 'or':
            self.write_code('D=D|M')
        else:
            raise Exception('incorrect command was received.')

        self.push_data()
            
    def binary_comp(self, command):
        self.pop2memory()
        self.write_code('D=M')
        self.pop2memory()
        l1 = self.get_new_label()
        l2 = self.get_new_label()

        if command == 'eq':
            jump = 'JEQ'
        elif command == 'gt':
            jump = 'JGT'
        elif command == 'lt':
            jump = 'JLT'
        else:
            raise Exception('incorrect command was received.')

        self.write_codes([
            'D=M-D',
            '@%s' % l1,
            'D;%s' % jump,
            'D=0',
            '@%s' % l2,
            '0;JMP',
            '(%s)' % l1,
            'D=-1',
            '(%s)' % l2
        ])

        self.push_data()
        
    def write_push_pop(self, command, segment, index):
        '''
        translate push/pop command.
        '''
        index = int(index)
        
        if command == C_PUSH:
            if segment == 'constant':
                self.push_constant(index)
            elif segment == 'static':
                self.push_static(index)                
            elif segment in ['local', 'argument', 'this', 'that']:
                self.push_builtin(segment, index)
            elif segment in ['pointer', 'temp']:
                self.push_address(segment, index)
            else:
                raise Exception('Received not defined segment.')
                
        elif command == C_POP:
            if segment == 'static':
                self.pop2static(index)
            elif segment in ['local', 'argument', 'this', 'that']:
                self.pop2builtin(segment, index)
            elif segment in ['pointer', 'temp']:
                self.pop2address(segment, index)
            else:
                raise Exception('Received not defined segment.')

        else:
            raise Exception('Call `write_push_pop` with not C_PUSH or C_POP. command')

    def push_constant(self, index):
        self.write_codes([
            '@%d' % index,
            'D=A'
        ])
        self.push_data()

    def push_static(self, index):
        self.write_codes([
            '@%s.%d' % (self.trans_file, index),
            'D=M'
        ])
        self.push_data()

    def pop2static(self, index):
        self.pop2memory()
        self.write_codes([
            'D=M',
            '@%s.%d' % (self.trans_file, index),
            'M=D'
        ])

    def push_builtin(self, segment, index):
        if segment == 'local':
            symbol = 'LCL'
        elif segment == 'argument':
            symbol = 'ARG'
        elif segment == 'this':
            symbol = 'THIS'
        elif segment == 'that':
            symbol = 'THAT'
        else:
            raise Exception('Received not defined segment.')
        
        self.write_codes([
            '@%s' % symbol,
            'A=M'
        ])
        for i in range(0, index):
            self.write_code('A=A+1')
        self.write_code('D=M')
        self.push_data()

    def pop2builtin(self, segment, index):
        if segment == 'local':
            symbol = 'LCL'
        elif segment == 'argument':
            symbol = 'ARG'
        elif segment == 'this':
            symbol = 'THIS'
        elif segment == 'that':
            symbol = 'THAT'
        else:
            raise Exception('Received not defined segment.')

        self.pop2memory()
        self.write_codes([
            'D=M',
            '@%s' % symbol,
            'A=M'
        ])
        for i in range(0, index):
            self.write_code('A=A+1')
        self.write_code('M=D')        

    def push_address(self, segment, index):
        if segment == 'pointer':
            base_addr = POINTER_BASE_ADDRESS
        elif segment == 'temp':
            base_addr = TEMP_BASE_ADDRESS
        else:
            raise Exception('Received not defined segment.')

        self.write_codes([
            '@%d' % base_addr
        ])
        for i in range(0, index):
            self.write_code('A=A+1')
        self.write_code('D=M')
        self.push_data()

    def pop2address(self, segment, index):
        if segment == 'pointer':
            base_addr = POINTER_BASE_ADDRESS
        elif segment == 'temp':
            base_addr = TEMP_BASE_ADDRESS
        else:
            raise Exception('Received not defined segment.')

        self.pop2memory()
        self.write_codes([
            'D=M',
            '@%d' % base_addr,
        ])
        for i in range(0, index):
            self.write_code('A=A+1')
        self.write_code('M=D')

    def push_data(self):
        '''
        push from D-register to Stack
        '''
        self.write_codes([
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ])

    def pop2memory(self):
        '''
        pop from Stack to D-register
        '''
        self.write_codes([
            '@SP',
            'M=M-1',
            'A=M'
        ])
    
    def write_code(self, code):
        self.fout.write(code + '\n')

    def write_codes(self, codes):
        self.write_code('\n'.join(codes))

    def get_new_label(self):
        self.label_num += 1
        return 'LABEL' + str(self.label_num)
