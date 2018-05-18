import os
import re
import errors as err

#pyparsing imports
from pyparsing import ParserElement, ParseFatalException
from pyparsing import Literal, Group, Regex, White, ZeroOrMore, OneOrMore, Optional, lineno
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
                    string += line.rstrip()
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

        def error(s, loc, expr, error):
            #TODO - Erreurs perso
            print('err')
            raise ParseFatalException(s, loc, err.DOCKERFILE_ERROR[211].format(ligne='{ligne}', colonne=loc, erreur=error.msg))


        #INIT
        ParserElement.setDefaultWhitespaceChars(" \t")

        #
        # TERMINALS
        #
        ALPHA = Regex(r'[A-Za-z]+')
        STR = Regex(r'\"(.*?)\"').setName('chaîne de caractères')
        NUM = Regex(r'[0-9]+').setName('numérique')
        ARG = Regex(r'\S+').setName('argument')
        COM = Regex(r'^#.*').setName('commentaire')

        SEP = White(' ', min=1).setName("espace").suppress()
        EOL = lineEnd().setName('fin de ligne').suppress()

        OH = Literal('[').suppress()
        CH = Literal(']').suppress()
        CO = Literal(',').suppress()
        PP = Literal(':').suppress()
        AS = Literal('AS').suppress()
        EQ = Literal('=').suppress()

        FROM = Literal('FROM')
        RUN = Literal('RUN')
        CMD = Literal('CMD')
        MAINTAINER = Literal('MAINTAINER')
        EXPOSE = Literal('EXPOSE')
        ENV = Literal('ENV')
        ADD = Literal('ADD') 
        COPY = Literal('COPY')
        ENTRYPOINT = Literal('ENTRYPOINT')
        WORKDIR = Literal('WORKDIR')

        #flag
        CHOWN = Literal('--chown=')

        #
        # NO TERMINALS
        #

        #Arguments
        t_args_table = OH - STR - ZeroOrMore(CO - STR) -  CH
        t_args_list = ARG - ZeroOrMore(ARG)
        t_args = t_args_table | t_args_list

        #Multiple lines separator
        continuation = '\\' - lineEnd()
        t_args_list.ignore(continuation)

        #FROM
        t_from_inst = FROM - Group(SEP - ARG - Optional(AS - SEP - ARG)) - EOL
        #RUN | CMD | ENTRYPOINT
        t_run_cmd_entrypoint_inst = (RUN | CMD | ENTRYPOINT) - Group(SEP - t_args) - EOL
        #MAINTAINER
        t_maintainer_workdir_inst = (MAINTAINER | WORKDIR) - Group(SEP - ARG) - EOL
        #EXPOSE
        t_expose_inst = EXPOSE - Group(OneOrMore(SEP - NUM - Optional(Literal('/tcp') | Literal('/udp')))) - EOL
        #ADD | COPY
        t_add_copy_inst = (ADD | COPY) - Group(SEP - Optional(CHOWN - ARG - SEP) - t_args) - EOL

        instructions = t_from_inst \
                    | t_run_cmd_entrypoint_inst \
                    | t_maintainer_workdir_inst \
                    | t_expose_inst \
                    | t_add_copy_inst

        return stringStart - Optional(COM | instructions) - stringEnd
