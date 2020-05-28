#!/usr/local/bin/python2.7
# encoding: utf-8
'''
eightanu.export_ascents -- An exporter of the new 8a.new ascents data.

eightanu.export_ascents is an exporter that scrap your ascents from the new 8a.nu website.

@author:     lordyavin

@copyright:  2020 lordyavin. All rights reserved.

@license:    MIT

@contact:    yavin@gmx.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from urllib3.response import HTTPResponse
from selenium.webdriver.remote.webelement import WebElement

__all__ = []
__version__ = 0.1
__date__ = '2020-05-27'
__updated__ = '2020-05-27'

DEBUG = 1
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


def export(username):
    from bs4 import BeautifulSoup    
    import urllib3

    url = "https://www.8a.nu/user/{username}/sportclimbing".format(username=username)    
        
    headers = {
        "Cookie": "_ga=GA1.2.1887139087.1544043139; __gads=ID=aca06ad9ff2a7aa5:T=1544043139:S=ALNI_MYiV0JPpCP9QPJsIi0GuBRQYOu_kA; __unam=613e139-16e125aa445-28740074-2; connect.sid=s%3AVkR8QNfd8z-ui4HIclR0e9xkxytVsbZF.WanzCGaabAsk4k6P2Snm84d7WlRUV%2Btap%2FZEzReQYi8"
    }
        
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    driver = webdriver.Firefox()
    driver.get(url)
    filters = driver.find_element_by_class_name("ascent-filters")
    assert isinstance(filters, WebElement)
    all_options  = filters.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "0":
            option.click()
    
    table = driver.find_element_by_class_name("user-ascents")
    assert isinstance(table, WebElement)
    
    table_headers = table.find_elements_by_tag_name("th")
    print( ", ".join([cell.text for cell in table_headers]) )
    
    rows = table.find_elements_by_tag_name("tr")
    for row in rows:
        cells = row.find_element_by_class_name("td")
        print( ", ".join([cell.text for cell in cells]) )
    
    driver.close()
    

def main(argv=None): # IGNORE:C0111
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

  Created by user_name on %s.
  Copyright 2020 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-u", "--user", dest="username", type=str, help="The 8a user name")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]", default=0)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        if verbose > 0:
            print("Verbose mode on")

        export(args.username)
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