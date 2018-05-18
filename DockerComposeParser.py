import os
import re
import config as config

#pyparsing imports
from pyparsing import ParserElement, ParseFatalException
from pyparsing import Literal, Group, Regex, White, ZeroOrMore, Optional, lineno
from pyparsing import stringStart, stringEnd, lineStart, lineEnd, SkipTo

class DockerComposeParser:
    def __init__(self):
        """DockerfileParser Class Constructor
   
        Check & Verify the syntax of a docker-compose.yml type file
     
     
        """
        self.fileparsed = list()
        self.error = list()
        self.grammar = self.docker_compose_grammar()


    def hasError(self):
        """Return True if errors"""
        if self.error:
            return True
        else:
            return False

    def parse(self, FilePath='./', Filename = 'docker-compose.yml'):
        pass

    def docker_compose_grammar(self):
        pass