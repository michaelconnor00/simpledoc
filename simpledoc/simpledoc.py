#!/usr/bin/env python

"""Docs to Markdown, simple

Usage:
    simpledoc.py (-path <path> | -file <filename>)

Options:
    --path <path>                           Path to the objects to be documented
    --file <version-file>                   Version file name [default: config.ini]
"""
import re
import os
import sys
import inspect
import pkgutil
import importlib
from getopt import getopt
import ConfigParser


OBJECTS_TO_DOCUMENT = []
PACKAGES = []


class Module(object):

    __is_package = None

    def __init__(self, kwargs, name=None):
        self.__module_name = self._check_name(name or kwargs.get('module_name'))
        self.__module_pkg_name = kwargs.get('module_pkg_name') or name or kwargs.get('module_name')
        self.__module = self.get_module()
        self.include_module = False if kwargs.get('include_module') == 'False' else True
        self.include_classes = False if kwargs.get('include_classes') == 'False' else True
        self.include_class_methods = False if kwargs.get('include_class_methods') == 'False' else True
        self.include_functions = False if kwargs.get('include_functions') == 'False' else True
        self.document_name = kwargs.get('document_name') or self.__module_name + '.md'
        self.__black_list = self._parse_blacklist(kwargs.get('black_list'))
        self.__is_package = self._is_package()
        if self.__is_package:
            if self.__module_pkg_name not in [x.package for x in PACKAGES]:
                PACKAGES.append(self)
        else:
            if self.__module_name not in [x.name for x in OBJECTS_TO_DOCUMENT]:
                OBJECTS_TO_DOCUMENT.append(self)

    @property
    def name(self):
        return self.__module_name

    @property
    def module(self):
        return self.__module

    @property
    def package(self):
        return self.__module_pkg_name

    @property
    def is_package(self):
        return self.__is_package

    def _check_name(self, name):
        if '.' in name:
            return name.split('.')[-1]
        else:
            return name

    def _is_package(self):
        # TODO This is important, yet unsure if it is accurate
        file_name = self.__module.__file__
        if '__init__' in file_name:
            return True
        else:
            return False

    def _parse_blacklist(self, string_list):
        if isinstance(string_list, list):
            return string_list
        if string_list is None:
            return []
        return string_list.replace(' ', '').split(',')

    def get_module(self):
        try:
            m = importlib.import_module(self.__module_pkg_name)
        except AttributeError:
            m = importlib.import_module(self.__module_name)
            self.__module_pkg_name = m.__name__
        return m

    def _check_black_list(self, pkg):
        for black_pkg in self.__black_list:
            if black_pkg == '':
                continue
            if pkg.startswith(black_pkg):
                # Don't add
                return True
        return False

    def flatten_submodules(self, module):
        """
        Turn all submodules into new Module objects.
        :param module: the string name of the module to flatten
        :return:
        """
        new_modules = self.get_submodules(module)
        for mod in new_modules:
            parts = mod[0].path.split('/')[1:]
            pkg_name = '.'.join(parts) + '.' + mod[1]
            mod_name = mod[1]
            is_package = mod[2]
            # print pkg_name, mod_name, is_package

            if self._check_black_list(pkg_name):
                continue

            Module(
                {
                    'module_name': mod_name,
                    'module_pkg_name': pkg_name,
                    'include_module': self.include_module,
                    'include_classes': self.include_classes,
                    'include_class_methods': self.include_class_methods,
                    'include_functions': self.include_functions,
                    'document_name': self.document_name,
                    'blacklist': self.__black_list
                }
            )

            if is_package:
                # Recurse down tree
                self.flatten_submodules(pkg_name)


    @staticmethod
    def get_submodules(module):
        if inspect.ismodule(module):
            return pkgutil.walk_packages(module.__path__)
        else:  # Assume string name
            return pkgutil.walk_packages([module])


def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    # while trimmed and not trimmed[-1]:  # NOTE this trims trailing spaces
    #     trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def h1(s):
    return '#'+s+'\n'

def h2(s):
    return '##'+s+'\n'

def h3(s):
    return '###'+s+'\n'

def h4(s):
    return '####'+s+'\n'


def gather_docstrings(doc):

    docstring_list = []

    if doc.include_module:
        docstring_list.append(
            DocString(doc.module.__doc__, 'module')
        )

    if doc.include_classes:
        classes = inspect.getmembers(doc.module, inspect.isclass)
        for c in classes:
            class_methods = inspect.getmembers(c[1], inspect.ismethod)
            class_functions = inspect.getmembers(c[1], inspect.isfunction)
            docstring_list.append(
                DocString(h2(c[0]) + trim(c[1].__doc__), 'class')
            )
            for m in class_methods:
                if m[0] == '__init__':
                    continue
                title = h3(c[0] + '.' + m[0])
                docstring_list.append(
                    DocString(title + trim(m[1].__doc__), 'class_method')
                )
            for f in class_functions:
                title = h3(c[0] + '.' + f[0])
                docstring_list.append(
                    DocString(title + trim(f[1].__doc__), 'function')
                )
        # FIXME This only goes one level deep. Won't pick up nested classes and so on.

    if doc.include_class_methods:
        methods = inspect.getmembers(doc.module, inspect.ismethod)
        for m in methods:
            title = h2(doc.name[0].capitalize() + doc.name[1:] + '.' + m[0])
            docstring_list.append(
                DocString(title + trim(m[1].__doc__), 'class_method')
            )

    if doc.include_functions:
        functions = inspect.getmembers(doc.module, inspect.isfunction)
        for f in functions:
            title = h2(doc.name[0].capitalize() + doc.name[1:] + '.' + f[0])
            docstring_list.append(
                DocString(title + trim(f[1].__doc__), 'function')
            )

    return docstring_list


class DocString(object):
    def __init__(self, docstring, obj_type):
        self.docstring = docstring
        self.obj_type = obj_type


def run(options, arguments, configs):
    section_list = configs.sections()

    for section in section_list:
        Module(dict(configs.items(section)), name=section)

    # Flatten all submodules
    for mod in PACKAGES:
        mod.flatten_submodules(mod.module)

    # print 'PKGS: ', [(x.name, x.package, x.is_package) for x in PACKAGES]
    # print 'TO_DOC: ', [(x.name, x.package, x.is_package) for x in OBJECTS_TO_DOCUMENT]

    for opt, val in options:
        # Look for options here
        overwrite = True if opt == '--overwrite' else False

    previous_filename = None
    for doc in OBJECTS_TO_DOCUMENT:

        print 'Writing %(mod)s docstrings to %(file)s' % {
            'file': doc.document_name,
            'mod': doc.name[0].capitalize() + doc.name[1:]
        }

        first_write = True

        if doc.document_name == previous_filename and os.path.isfile(doc.document_name) and first_write:
            method = 'a'
            first_write = False
        else:
            method = 'w'

        previous_filename = doc.document_name

        with open(doc.document_name, method) as outfile:
            docstrings = gather_docstrings(doc)
            for x in docstrings:
                outfile.write(x.docstring or '')
                outfile.write('\n')


if __name__ == '__main__':
    """Command-line interface"""

    shortopts = ''
    longopts = [
        'config=',
        'overwrite'
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
    # print config_path
    try:
        configs.read(config_path)
    except Exception as e:
        raise e  # TODO seems to fail silently

    # Scripts don't get the current directory in their path by default
    if '' not in sys.path:
        scriptdir = os.path.dirname(sys.argv[0])
        if scriptdir in sys.path:
            sys.path.remove(scriptdir)
        sys.path.insert(0, '.')

    run(opts, args, configs)
