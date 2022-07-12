#/usr/bin/env python3
"""

"""
from __future__ import annotations

import abc
import builtins
import datetime
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from functools import wraps
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

from acab_config.utils.log_formatter import AcabLogColourStripFormatter

if TYPE_CHECKING:
    # tc only imports
    pass

logging = logmod.getLogger(__name__)


def capture_printing():
    """
    Setup a file handler for a separate logger,
    to keep a trace of anything printed.
    Strips colour print command codes out of any string
    """
    oldprint = builtins.print
    # start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    TRACE_FILE_NAME = "trace.repl"
    input_trace_handler = logmod.FileHandler(TRACE_FILE_NAME, mode='w')
    input_trace_handler.setLevel(logmod.INFO)
    input_trace_handler.setFormatter(AcabLogColourStripFormatter(fmt='{message}'))

    trace_logger = logmod.getLogger('acab.repl.trace')
    trace_logger.setLevel(logmod.INFO)
    trace_logger.addHandler(input_trace_handler)
    trace_logger.propagate = False

    @wraps(oldprint)
    def intercepted(*args, **kwargs):
        """ Wraps `print` to also log to a separate trace file """
        oldprint(*args, **kwargs)
        if bool(args):
            trace_logger.warning(args[0])

    builtins.print = intercepted
