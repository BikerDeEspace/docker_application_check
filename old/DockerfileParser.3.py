import os
import re
import config as config

#pyparsing imports
from pyparsing import ParserElement, ParseFatalException
from pyparsing import Literal, Group, Regex, White, ZeroOrMore, Optional, lineno
from pyparsing import stringStart, stringEnd, lineStart, lineEnd, SkipTo

class DockerfileParser:
    def __init__(self):
        """DockerfileParser Class Constructor

        Check & Verify the syntax of a Dockerfile type file

        """
        self.fileparsed = list()
        self.error = list()
        self.grammar = self.dockerfile_instruction_grammar()

    def hasError(self):
        """Return True if errors"""
        if self.error:
            return True
        else:
            return False

    def parse(self, FilePath='./', Filename = 'Dockerfile'):
        """Parse
        
        Parsing of a Dockerfile file
        
        Params :
        FilePath -- Dockerfile directory (./ by default)
        Filename -- Dockerfile filename (Dockerfile by default)

        """
        self.error = list()
        self.file = FilePath + Filename

        # By default Pyparsing stops when he detect any error 
        # To get all errors we need to parse the file line by line
        if os.path.exists(self.file):
            with open(self.file, 'r') as file:
                lines = file.readlines()
                string = ''
                self.counter = 0
                for line in lines:
                    self.counter = self.counter + 1
                    string += line.strip(' ')
                    if not re.fullmatch(r".*\s\\\s*\n", line):
                        try:
                            result = self.grammar.parseString(string)
                            if result:
                                self.fileparsed.append(result)
                        except ParseFatalException as e:
                            self.error.append(str(e.msg))
                        string = ''
        else:
            self.error.append(config.DOCKERFILE_ERROR[200].format(chemin=self.file))
                        
    def dockerfile_instruction_grammar(self):
        """dockerfile_instruction_grammar"""

        #
        # Fail Action - Error template - Line / Col / Instruction 
        #
        def error(s, loc, expr, error):
            """Main error template"""
            raise ParseFatalException(config.DOCKERFILE_ERROR[210].format(ligne=self.counter, colonne=error.loc, inst=self.currentInstructionName, erreur=error.msg))

        #
        # Parse Action (Basic verification)
        #
        def instructions_parse(strng, loc, toks):
            """Check if the instruction exist in the config file"""

            self.currentInstructionName = toks[0]

            if toks[0] not in config.INSTRUCTION_CONFIG_LIST:
                raise ParseFatalException(config.DOCKERFILE_ERROR[201], loc=loc)

            self.currentInstruction = config.INSTRUCTION_CONFIG_LIST[toks[0]]

        def args_table_parse(strng, loc, toks):
            """Check if the table form is correct for the current instruction arguments"""

            if(self.currentInstruction[0] == 1):
                raise ParseFatalException(config.DOCKERFILE_ERROR[203], loc=loc)
        
        def args_list_parse(strng, loc, toks):
            """Check if the list form is correct for the current instruction arguments"""

            if(self.currentInstruction[0] == 2):
                raise ParseFatalException(config.DOCKERFILE_ERROR[204], loc=loc)
        
        def args_num_parse(strng, loc, toks):
            """Check if the number of arguments is correct"""

            minArg = self.currentInstruction[1]
            maxArg = self.currentInstruction[2]
            nbArgs = len(toks)
            if (not minArg <= nbArgs <= maxArg):
                raise ParseFatalException(config.DOCKERFILE_ERROR[205].format(nombre=nbArgs, min=minArg, max=maxArg), loc=loc)
  
        #INIT
        ParserElement.setDefaultWhitespaceChars(" \t")

        #
        # TERMINALS
        #
        INST = Regex(r'\S+').setParseAction(instructions_parse)
        STR = Regex(r'\"(.+?)\"').setName("chaîne de caractère")
        ARG = Regex(r'\S+').setName("argument")

        SEP = White(' ', min=1).setName("espace").suppress()
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
        
        t_args = SEP - (t_args_table | t_args_list)
        t_args.setParseAction(args_num_parse)

        #Multiple lines separator
        continuation = '\\' - lineEnd()
        t_args_list.ignore(continuation)
        t_args_table.ignore(continuation)



        #instruction grammar
        instruction = (stringStart - (COM | Optional(INST - Group(t_args))) - EOL - stringEnd()).setFailAction(error)

        return instruction