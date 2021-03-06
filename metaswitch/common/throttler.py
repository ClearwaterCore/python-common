# @file throttler.py
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


import logging
import threading
import time

_log = logging.getLogger("metaswitch.utils")

class Throttler:
    """Simple leaky-bucket throttler."""

    def __init__(self, rate_per_second, burst_count):
        """Constructor.

        Arguments:
        rate_per_second -- the maximum sustained event rate to allow
        per second.
        burst_count -- the maximum number of events to allow at once.
        """
        self._rate_per_second = rate_per_second
        self._burst_count = burst_count
        self._bucket = self._burst_count
        self._last_update = time.time()
        self._lock = threading.Lock()

    def is_allowed(self):
        """Attempt an event and determine if it is allowed.

        Returns True if it is allowed, and False if it is throttled.
        """
        with self._lock:
            now = time.time()
            delta = (now - self._last_update) * self._rate_per_second
            bucket = self._bucket + delta
            self._bucket = min(self._burst_count, bucket)
            self._last_update = time.time()
            # _log.debug("Bucket %f, last update %f", self._bucket, self._last_update)
            if self._bucket >= 1:
                self._bucket -= 1
                return True
            else:
                return False
            
    @property
    def interval_sec(self):
        """The typical sustained interval between events,
        as an integer number of seconds.

        Never less than 1."""
        return max(1, int(1 / self._rate_per_second))
