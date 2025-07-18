#!/usr/bin/python3

import logging
import time

__ALL__ = [ 'getLogger', 'log_extra' ]

getLogger = logging.getLogger


def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
               func=None, extra=None, sinfo=None):
    # logging.Logger
    rv = logging_makeRecord(self,
                            name, level, fn, lno, msg, args, exc_info,
                            func=func, extra=None, sinfo=sinfo)
    rv.extra = extra
    #print('Added extra', id(rv), extra)
    return rv

# `import logging` sets up root and manager as side effects.
# Workaround is to monkey patch the method on the class.
logging_makeRecord = logging.Logger.makeRecord
logging.Logger.makeRecord = makeRecord


class ExtraFormatter(logging.Formatter):
    converter = time.gmtime

    def formatMessage(self, record):
        base = super().formatMessage(record)
        if not record.extra:
            return base
        extra = [ '%s=%r' % key_value
                  for key_value in record.extra.items() ]
        return base + ' ' + ' '.join(extra)
    
# basicConfig accepts formatter=... starting in 3.15
logging.Formatter = ExtraFormatter


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    # XXX microseconds?
    #datefmt='%Y-%m-%d %H:%M_%S')
    #formatter=log_formatter)	# XXX py3.15
)


def log_extra(**kwargs):
    return {'extra': kwargs}

#--#
