import random
import sys
import logging
import re
from setuptools import setup

PYPY_SIMPLE_URL = 'https://pypi.python.org/simple/'

PY2 = sys.version_info < (3, 0)

if PY2:
    import urllib2 as urllib
else:
    import urllib

_log = logging.getLogger(__name__)


def get_packages(url):
    res = urllib.urlopen(url)

    pkg_re = re.compile(r'<a href=\'([^\']*)\'')
    packages = pkg_re.findall(res.read())
    _log.debug('\n'.join('packages: %s' % package for package in packages))
    return packages


def get_deps():
    _log.info('Getting possible dependencies. This may take a while if you '
              'are on a hotel wifi.')
    packages = get_packages(PYPY_SIMPLE_URL)

    number_of_deps = random.randint(3, 5)
    deps = random.sample(packages, number_of_deps)

    _log.info('You got \n- %s\nas dependenc(y|ies). Good luck!',
              '\n- '.join(deps))

    return deps


def main(argv=None):
    if argv and (len(argv) == 0 or argv[1] in ['egg_info']):
        deps = get_deps()
    else:
        deps = None

    setup(
        name='deproulette',
        version='1.0.3',
        author='Joar Wandborg',
        author_email='name \\x40 lastname. se',
        url='https://github.com/joar/deproulette',
        description='You never know what you get. Such is life.',
        long_description=open('README.rst').read(),
        install_requires=deps
    )


if __name__ == '__main__':
    import os
    print '\n'.join(get_deps())
    _log.setLevel(getattr(logging, os.environ.get('LOGLEVEL', 'INFO')))

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)

    def decorate_emit(fn):
    # add methods we need to the class
        def new(*args):
            levelno = args[0].levelno
            if levelno >= logging.CRITICAL:
                color = '\x1b[31;1m'
            elif levelno >= logging.ERROR:
                color = '\x1b[31;1m'
            elif levelno >= logging.WARNING:
                color = '\x1b[33;1m'
            elif levelno >= logging.INFO:
                color = '\x1b[32;1m'
            elif levelno >= logging.DEBUG:
                color = '\x1b[35;1m'
            else:
                color = '\x1b[0m'

            # add colored *** in the beginning of the message
            args[0].msg = "{0}***\x1b[0m {1}".format(color, args[0].msg)

            # new feature i like: bolder each args of message
            args[0].args = tuple('\x1b[1m' + arg + '\x1b[0m' for arg in args[0].args)
            return fn(*args)
        return new

    handler.emit = decorate_emit(handler.emit)

    _log.addHandler(handler)

    sys.exit(main(sys.argv))