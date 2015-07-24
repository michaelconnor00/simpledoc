#!/usr/bin/env python

"""Docs to Markdown, simple

Usage:
    simpledoc.py (-path <path> | -file <filename>)

Options:
    --path <path>                           Path to the objects to be documented
    --file <version-file>                   Version file name [default: config.ini]
"""
import pydoc
import os
import sys
import inspect
import pkgutil
import imp
import importlib
from getopt import getopt
import ConfigParser


OBJECTS_TO_DOCUMENT = []


class Module(object):

    def __init__(self, name, kwargs):
        self.__module_name = name
        self.__module = None
        self.__include_submodules = True if kwargs.get('include_submodules') == 'True' else False
        self.__include_classes = True if kwargs.get('include_classes') == 'True' else False
        self.__include_class_methods = True if kwargs.get('include_class_methods') == 'True' else False
        self.__include_functions = True if kwargs.get('include_functions') == 'True' else False
        self.__document_name = kwargs.get('document_name')  # TODO what if it is None
        self.__black_list = self._parse_blacklist(kwargs.get('black_list'))
        self.get_module()

    @property
    def name(self):
        return self.__module_name

    def _parse_blacklist(self, string_list):
        if isinstance(string_list, list):
            return string_list
        if string_list is None:
            return []
        return string_list.replace(' ', '').split(',')

    def get_module(self):
        m = importlib.import_module(self.__module_name)
        self.__module = m

    def flatten_submodules(self, module):
        """
        Turn all submodules into new Module objects.
        :param module: the string name of the module to flatten
        :return:
        """
        if self.__include_submodules:
            new_modules = self.get_submodules(module)
            for mod in new_modules:
                print mod[0], mod[1], mod[2]
                full_name = '{}.{}'.format(module.__name__, mod[1])
                if full_name in self.__black_list:
                    continue
                if full_name in [x.name for x in OBJECTS_TO_DOCUMENT]:
                    continue
                # If the module is not a package, add it.
                if not mod[2]:
                    OBJECTS_TO_DOCUMENT.append(
                        Module(
                            full_name,
                            {
                                'include_submodules': self.__include_submodules,
                                'include_classes': self.__include_classes,
                                'include_class_methods': self.__include_class_methods,
                                'include_functions': self.__include_functions,
                                'document_name': self.__document_name,
                                'blacklist': self.__black_list
                            }
                        )
                    )
                else:
                    self.flatten_submodules(mod[1])


    @staticmethod
    def get_submodules(module):
        return pkgutil.iter_modules(module.__path__)


def run(options, arguments, configs):
    section_list = configs.sections()

    for section in section_list:
        OBJECTS_TO_DOCUMENT.append(
            Module(section, dict(configs.items(section)))
        )

    # Flatten all submodules
    for mod in OBJECTS_TO_DOCUMENT:
        mod.flatten_submodules(mod.name)
    print 'TO_DOC: ', [x.name for x in OBJECTS_TO_DOCUMENT]
    # output_file = file('test.md', 'wb')

    subject_package = None
    subject_class = None
    for opt, val in options:
        # Look for options here
        if opt == '--class':
            subject_class = val
        if opt == '--pkg':
            subject_package = val


    # if subject_class:
    #     # TODO
    #     pass
    # elif subject_package:
    #     for name, data in inspect.getmembers(subject_package):
    #         if name == '__builtins__':
    #             continue
    #         if





if __name__ == '__main__':
    """Command-line interface"""

    shortopts = ''
    longopts = [
        'class=',
        'pkg=',
        'config='
    ]
    opts, args = getopt(
        sys.argv[1:],
        shortopts=shortopts,
        longopts=longopts
    )
    # __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __location__ = os.getcwd()

    config_file = 'config.ini'  # default file name

    for opt, val in opts:
        if opt == '--config':
            config_file = val

    config_path = os.path.join(__location__, config_file)
    configs = ConfigParser.ConfigParser()

    try:
        configs.read(config_path)
    except Exception as e:
        raise e  # TODO return proper message

    # Scripts don't get the current directory in their path by default
    if '' not in sys.path:
        scriptdir = os.path.dirname(sys.argv[0])
        if scriptdir in sys.path:
            sys.path.remove(scriptdir)
        sys.path.insert(0, '.')

    run(opts, args, configs)
