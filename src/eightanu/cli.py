#!/usr/local/bin/python3.6
# encoding: utf-8
'''
eightanu.cli -- The command line interface to export the new 8a.new ascents data.

eightanu.cli is an exporter that scrap your ascents from the new 8a.nu website.

@author:     lordyavin
@copyright:  2020 lordyavin. All rights reserved.
@license:    MIT
@contact:    github@klesatschke.net
@deffield    updated: Updated
'''
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import os
import sys

from eightanu import webdriver
from eightanu.export import export

__all__ = []
__version__ = 0.3
__date__ = '2020-05-27'
__updated__ = '2020-06-08'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by lordyavin on %s.
  Copyright 2020 lordyavin. All rights reserved.

  Licensed under the MIT License

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)        
        parser.add_argument("-b", "--browser", dest="browser", type=str, choices=webdriver.SUPPORTED_BROWSER, required=True)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]", default=0)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        parser.add_argument("username", type=str, help="Your 8a user name")

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        if verbose > 0:
            print("Verbose mode on")

        export(args.browser, args.username, verbose)
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'eightanu.export_ascents_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
