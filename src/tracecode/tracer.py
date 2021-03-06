#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/tracecode-build/
# The TraceCode software is licensed under the Apache License version 2.0.
# Data generated with TraceCode require an acknowledgment.
# TraceCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with TraceCode or any TraceCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with TraceCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  TraceCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  TraceCode is a free software build tracing tool from nexB Inc. and others.
#  Visit https://github.com/nexB/tracecode-build/ for support and download.

"""
TraceCode: trace a command execution with strace.
This is an incomplete work in progress.
"""

from __future__ import print_function
from __future__ import absolute_import

import os
import logging
import subprocess
import getopt
import sys
import errno


__version__ = '0.5.0'


logger = logging.getLogger('tracecode.trace')


def check_strace():
    pass


def check_disk_space():
    pass


def trace_command(cmd, output_dir):
    """
    Trace a command with strace.
    """
    prettycmd = ' '.join(cmd)
    logging.info('Tracing %(prettycmd)r to %(output_dir)s' % locals())
    trace_cmd = [
      'strace',  # TODO: should be an absolute path
      '-ff',  # trace each process and children in a separate trace file
      '-y',  # decode file descs
      '-s', '256',  # get so many chars per args.
      '-a1',  # no alignment for results codes
      '-qq',  # suppress process exit messages
      '-ttt',  # full resolution time stamps
      '-o', os.path.join(output_dir, 't'),  # output dir and trace name of 't'
      ] + cmd

    logging.debug('trace command: ' + ' '.join(trace_cmd))
    # TODO: capture stdout and stderr: tee to terminal and save in files
    proc = subprocess.Popen(trace_cmd)
    out = proc.communicate()[0]
    return proc.returncode, out


def usage():

    print('''
Trace a command execution and write results to a directory.

Usage:
    trace.py  -o DIR COMMAND
    trace.py  -h | --help | -v | --version

Arguments:
    COMMAND: the command to trace.

Options:
  -o, --output DIR  Existing directory where tracing is saved.
  -v, --version     Display current version, license and copyright notice.
  -h, --help        Display help.
''')


def version():
    print('''
TraceCode:tracer Version: %s
Copyright (c) 2017 nexB Inc. All rights reserved. https://github.com/nexB/tracecode-build
''' % __version__)


def check_dir(pth, label):
    if not os.path.exists(pth) or not os.path.isdir(pth):
        print('%s directory does not exist or is not a directory.' % (label,))
        sys.exit(errno.EEXIST)


def check_dir_empty(pth, label):
    if os.listdir(pth) :
        print('%s directory is not empty.' % (label,))
        sys.exit(errno.EEXIST)


def main(args, opts):
    logging.basicConfig(level=logging.INFO)
    if not len(args) <= 1:
        usage()
        sys.exit(0)

    opt = args[0]
    if opt in ('-h', '--help'):
        usage()
        sys.exit(0)
    elif opt in ('-v', '--version'):
        version()
        sys.exit(0)
    elif opt not in ('-o', '--output'):
        usage()
        sys.exit(errno.EINVAL)

    if not len(args) <= 3:
        print('Output directory and command are mandatory.')
        usage()
        sys.exit(errno.EINVAL)

    odir = args[1]
    output_dir = os.path.abspath(os.path.normpath(os.path.expanduser(odir)))
    if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
        print('Output directory %(odir)s does not exist or '\
              'is not a directory.' % locals())
        sys.exit(errno.EINVAL)
    if os.listdir(output_dir):
        print('Output directory %(odir)s must be empty.' % locals())
        sys.exit(errno.EINVAL)

    command = args[2:]
    trace_command(output_dir, command,)


if __name__ == '__main__':
    longopts = ['help', 'output', 'version', ]
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvo', longopts)
    except Exception, e:
        print(repr(e))
        usage()
        sys.exit(errno.EINVAL)

    main(args, opts)
