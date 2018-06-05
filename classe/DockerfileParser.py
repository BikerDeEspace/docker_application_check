import os
import re

from conf.constant import DOCKERFILE_FILENAMES
from conf.errors import DOCKERFILE_ERROR
from conf.instructions import INSTRUCTION_CONFIG_LIST, OPTIONAL_OPTION_CONFIG

from classe import DockerfileValidator

from pathlib import Path
from pyparsing import *


class DockerfileParser:
    """ Dockerfile
    Class who check & parse the instructions of a Dockerfile
    """
    def __init__(self, dockerfile_path='./', dockerfile_name=''):
        self.errors = list()
        self.result = list()

        self.validator = DockerfileValidator.DockerfileValidator(dockerfile_path)

        gen = (name for name in DOCKERFILE_FILENAMES if (dockerfile_path / name).exists)
        self.dockerfile_path = dockerfile_path / next(gen, dockerfile_name)


    def get_errors(self):
        return self.errors

    def get_result(self):
        return self.result


    def getlines(self):
        """Generator - Get lines of the file with continuation char"""
        self.line_counter = 0
        str_table = list()
        # By default Pyparsing stops when he detect any error 
        # To get all errors, we need to parse the file line by line
        with open(self.dockerfile_path, 'r') as file:
            for line in file.readlines():
                self.line_counter += 1
                str_table.append(line)
                if not re.fullmatch(r".*\s\\\s*\n", line):
                    yield " ".join(str_table)
                    str_table.clear()

    def check_dockerfile(self):
        if not os.path.exists(self.dockerfile_path):
            self.errors.append(DOCKERFILE_ERROR[200].format(chemin=self.dockerfile_path))
        else:
            for line in self.getlines():
                try:
                    parseLine = self.dockerfile_instruction_grammar().parseString(line)
                    if parseLine:
                        self.result.append([self.line_counter, parseLine])
                except ParseFatalException as e:
                    self.errors.append(str(e.msg))

        return True if not self.errors else False
                        
    def dockerfile_instruction_grammar(self):
        """dockerfile_instruction_grammar"""
        #
        # Fail Action - Error template - Line / Col / Instruction 
        #
        def error(s, loc, expr, error):
            """Main error template"""
            raise ParseFatalException(DOCKERFILE_ERROR[202].format(ligne=self.line_counter, colonne=error.loc, inst=self.currentInstructionName, erreur=error.msg))

        #
        # Parse Action (Basic verification)
        #

        def arg_validate(strng, loc, toks):
            """Do some verfications for the instruction arguments"""
            if not self.validator.validate_instruction(toks):
                raise ParseFatalException(self.validator.get_errors(), loc=loc)

        def instructions_parse(strng, loc, toks):
            """Check if the instruction exist in the config file"""

            self.currentInstructionName = toks[0]

            if toks[0] not in INSTRUCTION_CONFIG_LIST:
                raise ParseFatalException(DOCKERFILE_ERROR[211], loc=loc)

            self.currentInstruction = INSTRUCTION_CONFIG_LIST[toks[0]]

        def args_table_parse(strng, loc, toks):
            """Check if the table form is correct for the current instruction arguments"""

            if(self.currentInstruction[0] == 1):
                raise ParseFatalException(DOCKERFILE_ERROR[213], loc=loc)
        
        def args_list_parse(strng, loc, toks):
            """Check if the list form is correct for the current instruction arguments"""

            if(self.currentInstruction[0] == 2):
                raise ParseFatalException(DOCKERFILE_ERROR[214], loc=loc)
        
        def args_num_parse(strng, loc, toks):
            """Check if the number of arguments is correct"""

            minArg = self.currentInstruction[1]
            maxArg = self.currentInstruction[2]
            nbArgs = len(toks)
            if (not minArg <= nbArgs <= maxArg):
                raise ParseFatalException(DOCKERFILE_ERROR[215].format(nombre=nbArgs, min=minArg, max=maxArg), loc=loc)

        def opt_parse(strng, loc, toks):
            """Check if the option exist and if she's correct for the current instruction"""
            
            if toks[0] not in OPTIONAL_OPTION_CONFIG:
                raise ParseFatalException(DOCKERFILE_ERROR[216].format(opt=toks[0]), loc=loc)
            if self.currentInstructionName not in OPTIONAL_OPTION_CONFIG[toks[0]]:
                raise ParseFatalException(DOCKERFILE_ERROR[217].format(opt=toks[0]), loc=loc)


        #INIT
        ParserElement.setDefaultWhitespaceChars(" \t")

        #
        # TERMINALS
        #
        INST = Regex(r'([A-Z]+)(?<!\s)').setName('Instruction').setParseAction(instructions_parse)
        OPT = Regex(r'--[a-z]+=').setName('Option').setParseAction(opt_parse)

        STR = Regex(r'\"((.|\s)+?)\"').setName("chaîne de caractère")
        ARG = Regex(r'\S+').setName("argument")

        EOL = lineEnd().setName("fin de ligne").suppress()
        COM = Regex(r'#.*').suppress()
     
        OH = Literal('[').suppress()
        CH = Literal(']').suppress()
        CO = Literal(',').suppress() 

        #
        # NO TERMINALS
        #
        #Arguments
        t_args_table = OH - STR - ZeroOrMore(CO - STR) -  CH
        t_args_table.setName('["argument1", "argument2" …]')
        t_args_table.setParseAction(args_table_parse)

        t_args_list = ARG - ZeroOrMore(ARG)
        t_args_list.setName('argument1 argument2 …')
        t_args_list.setParseAction(args_list_parse)
        
        t_args = (t_args_table | t_args_list)
        t_args.setParseAction(args_num_parse)

        #Multiple lines separator
        continuation = '\\' - EOL

        #Optional elements
        t_opt = OneOrMore(OPT - Group(ARG))
        t_opt.setParseAction(opt_parse)

        #instruction
        instruction = (INST - Group(Optional(t_opt)) - Group(t_args)).setParseAction(arg_validate)

        #line grammar
        line = (stringStart - (COM | Optional(instruction)) - EOL - stringEnd()).setFailAction(error)
        
        line.ignore(continuation)

        return line