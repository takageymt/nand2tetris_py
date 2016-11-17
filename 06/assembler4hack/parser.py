'''
Parser for Hack-Assembly
'''

import re

# command type
A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

A_COMMAND_PATTERN = re.compile(r'@([0-9A-Za-z_\.\$:]+)')
L_COMMAND_PATTERN = re.compile(r'\(([0-9A-Za-z_\.\$:]+)\)')
C_COMMAND_PATTERN = re.compile(r'(?:(A?M?D?)=)?([^;]+)(?:;(.+))?')

class Parser():
    '''
    Parser for Hack-Assembly
    '''
    
    def __init__(self, filename):
        self.cur_cmd = None
        self.fin = open(filename, 'r')

    def __enter__(self):
        return self

    def __exit__(self, exp_type, exp_value, traceback):
        self.fin.close()

    def advance(self):
        '''
        read and set next command to current one.
        '''
        while True:
            # read 1 line from hack code
            line = self.fin.readline()
            if not line:
                self.cur_cmd = None
                break

            # delete spaces
            line_trimmed = line.strip().replace(' ', '')

            # delete comments
            comment_idx = line_trimmed.find('//')
            if comment_idx != -1:
                line_trimmed = line_trimmed[:comment_idx]

            # set current command
            if line_trimmed != '':
                self.cur_cmd = line_trimmed
                break

        return self.cur_cmd

    def command_type(self):
        '''
        notice current command type.
        '''
        if self.cur_cmd is None:
            raise Exception('Current command is Nothing.')
        elif self.cur_cmd[0] == '@':
            return A_COMMAND
        elif self.cur_cmd[0] == '(':
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        '''
        notice symbol of A_COMMAND or L_COMMAND
        '''
        # check command type
        cmd_type = self.command_type()
        if cmd_type == A_COMMAND:
            # @Xxx
            m = A_COMMAND_PATTERN.match(self.cur_cmd)
            if not m:
                raise Exception('Symbol Parse Error: A_COMMAND')
            return m.group(1)
        
        elif cmd_type == L_COMMAND:
            # (Xxx)
            m = L_COMMAND_PATTERN.match(self.cur_cmd)
            if not m:
                raise Exception('Symbol Parse Error: L_COMMAND')
            return m.group(1)
        else:
            raise Exception('Current command is not A_COMMAND or L_COMMAND')

    def dest(self):
        '''
        notice dest mnemonic of C_COMMAND
        '''
        # check command type
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            # [dest]=comp;jump            
            m = C_COMMAND_PATTERN.match(self.cur_cmd)
            if not m:
                raise Exception('Mnemonic Parse Error: C_COMMAND')
            return m.group(1)
        else:
            raise Exception('Current command is not C_COMMAND')

    def comp(self):
        '''
        notice comp mnemonic of C_COMMAND
        '''
        # check command type
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            # dest=[comp];jump
            m = C_COMMAND_PATTERN.match(self.cur_cmd)
            if not m:
                raise Exception('Mnemonic Parse Error: C_COMMAND')
            return m.group(2)
        else:
            raise Exception('Current command is not C_COMMAND')        

    def jump(self):
        '''
        notice jump mnemonic of C_COMMAND
        '''
        # check command type
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            # dest=comp;[jump]
            m = C_COMMAND_PATTERN.match(self.cur_cmd)
            if not m:
                raise Exception('Mnemonic Parse Error: C_COMMAND')
            return m.group(3)
        else:
            raise Exception('Current command is not C_COMMAND')        
        
