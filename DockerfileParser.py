import os
import re
import errors as err

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
        """hasError
        
        Return True if errors
        
        """
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

        #On verifie que le fichier existe
        if os.path.exists(self.file):
            #On ouvre le fichier
            with open(self.file, 'r') as file:
                #On recupère les lignes
                lines = file.readlines()
                string = ''
                counter = 0
                #Pour chaque lignes
                for line in lines:
                    counter = counter + 1
                    string += line
                    #Si elle ne se termine pas par un antislash on parse l'instruction
                    if not re.fullmatch(r".*\\\s*\n", line):
                        try:
                            result = self.grammar.parseString(string)
                            if result:
                                self.fileparsed.append(result)
                        except ParseFatalException as e:
                            self.error.append(str(e.msg).format(ligne=counter))
                        string = ''
        else:
            self.error.append(err.DOCKERFILE_ERROR[200].format(chemin=self.file))
                        
    def dockerfile_instruction_grammar(self):
        """dockerfile_instruction_grammar"""

        #
        # Parse Action (Basic verification)
        #
        def instructions_parse(strng, loc, toks):
            """Check if the instruction exist"""
            #InstructionName : [ArgumentsFormCode, ArgumentsNumMin, ArgumentsNumMax]
            #ArgumentsFormCode :
            # -- 1: Simple List forms (Ex: arg1 arg2)
            # -- 2: Table forms (Ex: ["arg1", "arg2"])
            # -- 3: All possible forms
            instructions = {
                'FROM': [1, 1, 1], 
                'RUN': [3, 1, 20], 
                'ADD': [2, 2, 2], 
                'COPY': [1, 2, 2], 
                'EXPOSE': [1, 1, 1], 
                'CMD': [3, 1, 3], 
                'ENTRYPOINT': [3, 1, 3], 
                'VOLUME': [3, 1, 1], 
                'WORKDIR': [3, 1, 1]
            }
            if toks[0] not in instructions:
                raise ParseFatalException(err.DOCKERFILE_ERROR[201].format(ligne='{ligne}', colonne=loc, inst=toks[0]))
            self.currentInstruction = instructions[toks[0]]

        def args_table_parse(strng, loc, toks):
            """Check if the table form is correct for the current instruction arguments"""

            if(self.currentInstruction[0] == 1):
                raise ParseFatalException(err.DOCKERFILE_ERROR[204].format(ligne='{ligne}', colonne=loc))
        
        def args_list_parse(strng, loc, toks):
            """Check if the list form is correct for the current instruction arguments"""

            if(self.currentInstruction[0] == 2):
                raise ParseFatalException(err.DOCKERFILE_ERROR[203].format(ligne='{ligne}', colonne=loc))
        
        def args_num_parse(strng, loc, toks):
            """Check if the number of arguments is correct"""

            minArg = self.currentInstruction[1]
            maxArg = self.currentInstruction[2]
            nbArgs = len(toks)
            if (not minArg <= nbArgs <= maxArg):
                raise ParseFatalException(err.DOCKERFILE_ERROR[205].format(ligne='{ligne}', colonne=loc, nombre=nbArgs, min=minArg, max=maxArg))
        #INIT
        ParserElement.setDefaultWhitespaceChars(" \t")

        #
        # TERMINALS
        #
        INST = Regex(r'[A-Z]+').setParseAction(instructions_parse)
        STR = Regex(r'\"(.*?)\"')
        ARG = Regex(r'\S+')
        COM = Regex(r'#.*').suppress()

        SEP = White(' ', min=1).setName('INST [arguments]').suppress()
        EOL = lineEnd().suppress()

        OH = Literal('[').suppress()
        CH = Literal(']').suppress()
        CO = Literal(',').suppress()

        #
        # NO TERMINALS
        #
        #Arguments
        t_args_table = (OH - STR - ZeroOrMore(CO - STR) -  CH).setParseAction(args_table_parse)
        t_args_list = (ARG - ZeroOrMore(SEP - Optional(ARG))).setParseAction(args_list_parse)
        t_args = SEP - ((t_args_table | t_args_list)).setParseAction(args_num_parse).setName('INST [arguments]')

        #Multiple lines separator
        continuation = '\\' - lineEnd()
        t_args_list.ignore(continuation)

        #instruction grammar
        instruction = stringStart - Optional(SEP) - Optional(COM | (INST - Group(t_args))) - EOL - stringEnd()
        
        return instruction