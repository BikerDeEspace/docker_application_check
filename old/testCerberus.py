import yaml
import config as config

from cerberus import Validator

#
# Docker-compose schema
#
schema = {
    'version': {
        'type': 'string'
    },
    'services': {
        'type': 'dict',
        'keyschema' : {
            'type': 'string',
            'regex': '[a-z]+'
        },
        'valueschema': {
            'type': 'dict',
            'schema': {
                #BUILD
                'build': {
                    "oneof": [
                        #Short Syntax 
                        {   
                            'type': 'string'
                        },
                        #Long Syntax
                        {
                            'type': 'dict',
                            'schema': {
                                'context': {
                                    'type': 'string'
                                },
                                'dockerfile': {
                                    'type': 'string'
                                },
                                'args': {
                                    'type': ['dict', 'list'],
                                    'schema': {
                                        'buildno': {
                                            'type': 'integer'
                                        },
                                        'gitcommithash': {
                                            'type': 'string'
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    'excludes': 'image',
                    'required': True
                },
                #IMAGE
                'image': {
                    'type': 'string',
                    'excludes': 'build',
                    'required': True
                },
                #PORTS
                'ports': {
                    "oneof": [
                        #Short Syntax 
                        {
                            'type': 'list',
                            'schema': {
                                'type': 'string'
                            }
                        },
                        #Long Syntax
                        {
                            'type': 'dict',
                            'schema': {
                                'target': {
                                    'type': 'integer'
                                },
                                'published': {
                                    'type': 'integer'
                                },
                                'protocol': {
                                    'type': 'string' #tcp | udp
                                },
                                'mode': {
                                    'type': 'string'
                                }
                            }
                        }
                    ]
                },
                #CONFIGS
                'configs': {
                    "oneof": [
                        {
                            'type': 'list',
                            'schema': {
                                'type': 'string'
                            }
                        },
                        {
                            'type': 'dict',
                            'schema': {
                                'source': {
                                    'type': 'string'
                                },
                                'target': {
                                    'type': 'string'
                                },
                                'uid': {
                                    'type': 'string'
                                },
                                'gid': {
                                    'type': 'string'
                                },
                                'mode': {
                                    'type': 'integer'
                                }
                            }
                        }
                    ]
                },
                #CONTAINER_NAME
                'container_name': {
                    'type': 'string'
                }
            }
        }
    },
    'configs': {
        'type': 'dict',
        'keyschema' : {
            'type': 'string',
            'regex': '[a-z]+'
        },
        'valueschema': {
            'type': 'dict',
            'schema': {
                'file': {
                    'type': 'string',
                    'excludes': 'external',
                    'required': True
                },
                'external': {
                    'type': 'boolean',
                    'excludes': 'file',
                    'required': True
                }
            }
        }
    }
}

with open("docker-compose.yml", 'r') as stream:
    try:
        doc = yaml.load(stream)

        v = Validator(schema)
        print(v.validate(doc, schema))
        
        print(v.errors)
    except yaml.YAMLError as exception:
        raise exception