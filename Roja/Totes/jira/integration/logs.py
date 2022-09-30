# Copyright 2017 Atlassian
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import traceback
from copy import copy
from logging import getLogger
from logging.config import dictConfig

from gunicorn.instrument.statsd import Statsd
from statsd import StatsClient

from prlinks import settings

dictConfig(copy(settings.LOGGING))

__all__ = ['getLogger', 'GunicornLogger']


statsd = StatsClient(host=settings.STATSD_HOST, port=settings.STATSD_PORT,
                     prefix=settings.STATSD_PREFIX)


class GunicornLogger(Statsd):
    """Logger used by the gunicorn server.

    The purpose of this logger is for access logging. The reason for having
    this logger (instead of just using the Django logger) is because this
    operates at the Gunicorn level and hence is able to log even cached
    requests. Specifically, when the cache headers in a request indicate
    that the browser does indeed have the correct version of the page,
    this logger will record the request, while the Django level logger
    wouldn't see the request.
    """

    def setup(self, cfg):
        # No need to hardwire Python logging here as we're setting up logging
        # ourselves and are using nginx's logs instead of gunicorn's.
        pass

    def now(self):
        return time.strftime('%Y-%m-%dT%H:%M:%S%z')

    def atoms(self, resp, req, environ, request_time):
        glogger_atoms = super(GunicornLogger, self).atoms(
            resp=resp, req=req, environ=environ, request_time=request_time)

        status = resp.status.split(None, 1)[0]
        maybe_nones = {
            'date': self.now(),
            'remote_address': environ.get('REMOTE_ADDR'),
            'user_agent': environ.get('HTTP_USER_AGENT'),
            'referrer': environ.get('HTTP_REFERER'),
            'request.method': environ.get('REQUEST_METHOD'),
            'request.path': environ.get('RAW_URI'),
            'request.time': "%d.%06d" % (request_time.seconds,
                                         request_time.microseconds),
            'response.len': resp.sent,
            'response.status': status,
            'sentry.id': glogger_atoms.get('{x-sentry-id}o')
        }

        return {k: v for k, v in maybe_nones.items() if v is not None}

    def access(self, resp, req, environ, request_time):
        """Override the superclass' access to circumvent the restrictions of
        access_log_format.

        Gunicorn's access_log_format forces you to include atoms even when
        they are `None` by replacing them with `-`. That is not acceptable.
        """
        if not self.cfg.accesslog and not self.cfg.logconfig:
            return

        # safe_atoms come from the original base class
        safe_atoms = self.atoms_wrapper_class(
            super(GunicornLogger, self).atoms(
                resp, req, environ, request_time))

        # atoms are things we want to pull out, with better names
        atoms = self.atoms(resp, req, environ, request_time)

        # Grabbed code from statsd itself. The reason is so we can only do the
        # stats and not need to also call the parent access logger.
        duration_in_ms = (request_time.seconds * 1000 +
                          float(request_time.microseconds) / 10 ** 3)

        status = resp.status
        if isinstance(status, str):
            status = int(status.split(None, 1)[0])

        self.histogram("gunicorn.request.duration", duration_in_ms)
        self.increment("gunicorn.requests", 1)
        self.increment("gunicorn.request.status.%d" % status, 1)

        try:
            self.access_log.info(self.cfg.access_log_format % safe_atoms,
                                 extra=atoms)
        except:
            self.error(traceback.format_exc())