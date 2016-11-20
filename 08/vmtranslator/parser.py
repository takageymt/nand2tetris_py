'''
Parser for .vm
'''

from constants import *

class Parser():
    '''
    Parser for .vm
    '''
    def __init__(self, filename):
        self.curr_cmd = None
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
            # read 1 line from vm code
            line = self.fin.readline()
            if not line:
                self.curr_cmd = None
                break

            # delete spaces
            line_trimmed = line.strip()

            # delete comments
            comment_idx = line_trimmed.find('//')
            if comment_idx != -1:
                line_trimmed = line_trimmed[:comment_idx]

            # set current command
            if line_trimmed != '':
                self.curr_cmd = line_trimmed.split()
                break

        return self.curr_cmd

    def command_type(self):
        '''
        notice current command type.
        '''
        if self.curr_cmd is None:
            raise Exception('Current command is Nothing.')
        elif self.curr_cmd[0] == 'push':
            return C_PUSH
        elif self.curr_cmd[0] == 'pop':
            return C_POP
        elif self.curr_cmd[0] == 'label':
            return C_LABEL
        elif self.curr_cmd[0] == 'goto':
            return C_GOTO
        elif self.curr_cmd[0] == 'if-goto':
            return C_IF
        elif self.curr_cmd[0] == 'function':
            return C_FUNCTION
        elif self.curr_cmd[0] == 'return':
            return C_RETURN        
        elif self.curr_cmd[0] == 'call':
            return C_CALL
        elif self.curr_cmd[0] in ['add', 'sub', 'neg', 'eq',
                                  'gt', 'lt', 'and', 'or', 'not']:
            return C_ARITHMETIC
        else:
            raise Exception('Command does not exist.')
    

    def arg1(self):
        '''
        return first argument.
        '''
        cmd_type = self.command_type()
        if cmd_type == C_RETURN:
            raise Exception('Command does not have 1st argument.')
        
        elif cmd_type == C_ARITHMETIC:
            return self.curr_cmd[0]
        
        elif cmd_type in [C_PUSH, C_POP, C_FUNCTION,
                        C_CALL, C_LABEL, C_GOTO, C_IF]:
            return self.curr_cmd[1]
        
        else:
            raise Exception('Command is Not Found.')
        
    def arg2(self):
        '''
        return second argument.
        '''
        cmd_type = self.command_type()
        if cmd_type in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            return self.curr_cmd[2]
        
        else:
            raise Exception('Command does not have 2nd argument.')

    
