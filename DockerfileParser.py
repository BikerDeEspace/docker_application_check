import os
import re
import config as config

from pathlib import Path

#pyparsing imports
from pyparsing import *

class DockerfileParser:
    def __init__(self):
        """DockerfileParser Class Constructor

        Check & Verify the syntax of a Dockerfile type file

        """
        self.fileparsed = list()
        self.error = list()
        self.grammar = self.dockerfile_instruction_grammar()

    def parse(self, FilePath='./', Filename=''):
        """Parse
        
        Parsing of a Dockerfile file
        
        Params :
        FilePath -- Dockerfile directory (./ by default)
        Filename -- Dockerfile filename (Dockerfile by default)

        """

        # By default Pyparsing stops when he detect any error 
        # To get all errors, we need to parse the file line by line
        def getlines(file):
            """Generator - Get lines of the file with continuation char"""
            self.line_counter = 0
            str_table = list()
            for line in file.readlines():
                self.line_counter += 1
                str_table.append(line)
                if not re.fullmatch(r".*\s\\\s*\n", line):
                    yield " ".join(str_table)
                    str_table.clear()

        #Check Dockerfile default names
        gen = (name for name in config.DOCKERFILE_FILENAMES if (FilePath / name).exists)
        self.file = FilePath / next(gen, Filename)

        if not os.path.exists(self.file):
            self.error.append(config.DOCKERFILE_ERROR[200].format(chemin=self.file))
        else:
            #Parsing line by line
            with open(self.file, 'r') as file:
                for line in getlines(file):
                    try:
                        parseLine = self.grammar.parseString(line)
                        if parseLine:
                            self.fileparsed.append([self.line_counter, parseLine])
                    except ParseFatalException as e:
                        self.error.append(str(e.msg))

        return self.error
                        
    def dockerfile_instruction_grammar(self):
        """dockerfile_instruction_grammar"""
        #
        # Fail Action - Error template - Line / Col / Instruction 
        #
        def error(s, loc, expr, error):
            """Main error template"""
            raise ParseFatalException(config.DOCKERFILE_ERROR[202].format(ligne=self.line_counter, colonne=error.loc, inst=self.currentInstructionName, erreur=error.msg))

        #
        # Parse Action (Basic verification)
        #
        def instructions_parse(strng, loc, toks):
            """Check if the instruction exist in the config file"""

            self.currentInstructionName = toks[0]

            if toks[0] not in config.INSTRUCTION_CONFIG_LIST:
                raise ParseFatalException(config.DOCKERFILE_ERROR[211], loc=loc)

            self.currentInstruction = config.INSTRUCTION_CONFIG_LIST[toks[0]]

        def args_table_parse(strng, loc, toks):
            """Check if the table form is correct for the current instruction arguments"""

            if(self.currentInstruction[0] == 1):
                raise ParseFatalException(config.DOCKERFILE_ERROR[213], loc=loc)
        
        def args_list_parse(strng, loc, toks):
            """Check if the list form is correct for the current instruction arguments"""

            if(self.currentInstruction[0] == 2):
                raise ParseFatalException(config.DOCKERFILE_ERROR[214], loc=loc)
        
        def args_num_parse(strng, loc, toks):
            """Check if the number of arguments is correct"""

            minArg = self.currentInstruction[1]
            maxArg = self.currentInstruction[2]
            nbArgs = len(toks)
            if (not minArg <= nbArgs <= maxArg):
                raise ParseFatalException(config.DOCKERFILE_ERROR[215].format(nombre=nbArgs, min=minArg, max=maxArg), loc=loc)
  
        def opt_parse(strng, loc, toks):
            """Check if the option exist and if she's correct for the current instruction"""
            
            if toks[0] not in config.OPTIONAL_OPTION_CONFIG:
                raise ParseFatalException(config.DOCKERFILE_ERROR[216].format(opt=toks[0]), loc=loc)
            if self.currentInstructionName not in config.OPTIONAL_OPTION_CONFIG[toks[0]]:
                raise ParseFatalException(config.DOCKERFILE_ERROR[217].format(opt=toks[0]), loc=loc)


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
        instruction = INST - Group(Optional(t_opt)) - Group(t_args)

        #line grammar
        line = (stringStart - (COM | Optional(instruction)) - EOL - stringEnd()).setFailAction(error)
        
        line.ignore(continuation)

        return line