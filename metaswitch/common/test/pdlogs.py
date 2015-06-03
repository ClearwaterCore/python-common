# @file utils.py
#
# Project Clearwater - IMS in the Cloud
# Copyright (C) 2013  Metaswitch Networks Ltd
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version, along with the "Special Exception" for use of
# the program along with SSL, set forth below. This program is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
#
# The author can be reached by email at clearwater@metaswitch.com or by
# post at Metaswitch Networks Ltd, 100 Church St, Enfield EN2 6BQ, UK
#
# Special Exception
# Metaswitch Networks Ltd  grants you permission to copy, modify,
# propagate, and distribute a work formed by combining OpenSSL with The
# Software, or a work derivative of such a combination, even if such
# copying, modification, propagation, or distribution would otherwise
# violate the terms of the GPL. You must comply with the GPL in all
# respects for all of the code used other than OpenSSL.
# "OpenSSL" means OpenSSL toolkit software distributed by the OpenSSL
# Project and licensed under the OpenSSL Licenses, or a work based on such
# software and licensed under the OpenSSL Licenses.
# "OpenSSL Licenses" means the OpenSSL License and Original SSLeay License
# under which the OpenSSL Project distributes the OpenSSL toolkit software,
# as those licenses appear in the file LICENSE-OPENSSL.

import unittest
import mock
import syslog
from metaswitch.common.pdlogs import PDLog

class PDLogTestCase(unittest.TestCase):
    @mock.patch("syslog.syslog")
    def testLogWithParams(self, mock_syslog):
        TEST_LOG = PDLog(desc="This is a test log",
                         cause="A test has been run",
                         effect="You will be confident that {acronym} logs work",
                         action="Check if this test passes",
                         priority=PDLog.LOG_NOTICE)
        TEST_LOG.log(acronym="ENT")
        mock_syslog.assert_called_with(PDLog.LOG_NOTICE, "Description: This is a test log. @@Cause: A test has been run. @@Effect: You will be confident that ENT logs work. @@Action:  Check if this test passes.")


    @mock.patch("syslog.syslog")
    def testLogWithoutParams(self, mock_syslog):
        TEST_LOG = PDLog(desc="This is a test log",
                         cause="A test has been run",
                         effect="You will be confident that PD logs work",
                         action="Check if this test passes",
                         priority=PDLog.LOG_NOTICE)
        TEST_LOG.log()
        mock_syslog.assert_called_with(PDLog.LOG_NOTICE, "Description: This is a test log. @@Cause: A test has been run. @@Effect: You will be confident that PD logs work. @@Action:  Check if this test passes.")
