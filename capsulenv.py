#!/usr/bin/env python

from capsule import Capsule
from docopt import docopt

import logging

DOCS = """Manage capsule environments.

Usage:
  capsulenv make <name> [options]
  capsulenv workon <name> [options]
  capsulenv remove <name> [options]
  capsulenv list [options]
  capsulenv save <name> [options]
  capsulenv load <filename> <name>
  capsulenv pyhistory <name>

Options:
  --baseimage

  --debug       Print debug messages.
  -h --help     Show this screen.
  --version     Show version.
"""

VERSION = "1"

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, format='[%(levelname)s] %(asctime)s %(message)s')

    arguments = docopt(DOCS, version=VERSION)

    if arguments['--debug']:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('docker').setLevel(logging.DEBUG)
    else:
        logging.getLogger('docker').setLevel(logging.WARNING)

    if arguments['list']:
        cap = Capsule(None)
        for c in cap.list():
            print(c)
    elif arguments['make']:
        cap = Capsule(arguments['<name>'])
        cap.start()
        cap.stop()
    elif arguments['workon']:
        cap = Capsule(arguments['<name>'])
        cap.start()
        print("Press Enter to activate this capsule...")
        cap.activate()
    elif arguments['remove']:
        cap = Capsule(arguments['<name>'])
        cap.remove()
    elif arguments['save']:
        cap = Capsule(arguments['<name>'])
        cap.export()
    elif arguments['pyhistory']:
        cap = Capsule(arguments['<name>'])
        cap.pyhistory()
