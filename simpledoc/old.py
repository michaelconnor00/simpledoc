"""Docs to Markdown, simple

Usage:
    simpledoc.py (-path <path> | -file <filename>)

Options:
    --path <path>                           Path to the objects to be documented
    --file <version-file>                   Version file name [default: config.ini]
"""

import os
import sys
import inspect
import __builtin__
from pydoc import (
    safeimport,
    ispath,
    importfile,
    ErrorDuringImport,
    describe,
    _OLD_INSTANCE_TYPE,
    text,
    pager,
    Helper
)
from getopt import getopt
import ConfigParser

# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
# versionpath = os.path.join(__location__, 'config.ini')
# version_file = versionpath
# versions_config = ConfigParser.ConfigParser()
# versions_config.read(version_file)

def locate(path, forceload=0):
    """Locate an object by name or dotted path, importing as necessary."""
    parts = [part for part in path.split('.') if part]
    print parts
    module, n = None, 0
    while n < len(parts):
        nextmodule = safeimport('.'.join(parts[:n+1]), forceload)
        if nextmodule: module, n = nextmodule, n + 1
        else: break
    if module:
        object = module
    else:
        object = __builtin__
    for part in parts[n:]:
        try:
            object = getattr(object, part)
        except AttributeError:
            return None
    return object

def resolve(thing, forceload=0):
    """Given an object or a path to an object, get the object and its name."""
    if isinstance(thing, str):
        object = locate(thing, forceload)
        if not object:
            raise ImportError, 'no Python documentation found for %r' % thing
        return object, thing
    else:
        name = getattr(thing, '__name__', None)
        return thing, name if isinstance(name, str) else None

def render_doc(thing, title='Python Library Documentation: %s', forceload=0):
    """Render text documentation, given an object or a path to an object."""
    object, name = resolve(thing, forceload)
    desc = describe(object)
    module = inspect.getmodule(object)
    if name and '.' in name:
        desc += ' in ' + name[:name.rfind('.')]
    elif module and module is not object:
        desc += ' in module ' + module.__name__
    if type(object) is _OLD_INSTANCE_TYPE:
        # If the passed object is an instance of an old-style class,
        # document its available methods instead of its value.
        object = object.__class__
    elif not (inspect.ismodule(object) or
              inspect.isclass(object) or
              inspect.isroutine(object) or
              inspect.isgetsetdescriptor(object) or
              inspect.ismemberdescriptor(object) or
              isinstance(object, property)):
        # If the passed object is a piece of data or an instance,
        # document its available methods instead of its value.
        object = type(object)
        desc += ' object'
    return title % desc + '\n\n' + text.document(object, name)

def doc(thing, title='Python Library Documentation: %s', forceload=0):
    """Display text documentation, given an object or a path to an object."""
    try:
        pager(render_doc(thing, title, forceload))
    except (ImportError, ErrorDuringImport), value:
        print value

class SimpleHelper(Helper):
    """
    Extension of pydoc Helper class to condition output for markdown
    """

    def help(self, request):
        if type(request) is type(''):
            print 'STRING: ', request
            request = request.strip()
            if request == 'help':
                self.intro()
            elif request == 'keywords':
                self.listkeywords()
            elif request == 'symbols':
                self.listsymbols()
            elif request == 'topics':
                self.listtopics()
            elif request == 'modules':
                self.listmodules()
            elif request[:8] == 'modules ':
                self.listmodules(request.split()[1])
            elif request in self.symbols:
                self.showsymbol(request)
            elif request in self.keywords:
                self.showtopic(request)
            elif request in self.topics:
                self.showtopic(request)
            elif request:
                doc(request, 'Help on %s:')
        elif isinstance(request, Helper):
            print 'HERE1'
            self()
        else:
            print 'HERE2'
            doc(request, 'Help on %s:')
        self.output.write('\n')


def cli(options, arguments):
    # Scripts don't get the current directory in their path by default
    # unless they are run with the '-m' switch
    if '' not in sys.path:
        scriptdir = os.path.dirname(sys.argv[0])
        if scriptdir in sys.path:
            sys.path.remove(scriptdir)
        sys.path.insert(0, '.')

    output_file = file('test.md', 'wb')

    subject_filename = None
    subject_path = None
    subject_package = None
    for opt, val in options:
        # Look for options here
        if opt == '--file':
            subject_filename = val
        if opt == '--path':
            subject_path = val
        if opt == '--pkg':
            subject_package = val


    if subject_filename:
        # Check if the filename exists
        if ispath(subject_filename) and not os.path.exists(subject_filename):
            print 'File %r does not exist' % subject_filename
        try:
            # if ispath(subject_filename) and os.path.isfile(subject_filename):
            #     arg = importfile(subject_filename)
            helper = SimpleHelper(output=output_file)
            helper.help(subject_filename)
            output_file.close()
        except ErrorDuringImport, value:
            print 'EXCEPTION: ', value
    elif subject_package:
        for name, data in inspect.getmembers(subject_package):
            if name == '__builtins__':
                continue





if __name__ == '__main__':
    """Command-line interface (looks at sys.argv to decide what to do)."""
    shortopts = ''
    longopts = [
        'file=',
        'path=',
        'pkg='
    ]
    opts, args = getopt(
        sys.argv[1:],
        shortopts=shortopts,
        longopts=longopts
    )
    cli(opts, args)
