#!/usr/bin/env python3
from __future__ import annotations

import logging as logmod

from acab_config.error.config_error import AcabConfigException
from acab_config.utils.log_formatter import (AcabLogFormatter, AcabLogRecord,
                                             AcabMinimalLogRecord,
                                             AcabNameTruncateFormatter)
from acab_config.utils.sorting import priority

logging = logmod.getLogger(__name__)

@priority(0)
def log_hook(self):
    """
    Config Hook to install AcabLog Formatting and Record types into
    the logging system
    """
    try:
        spec     = self.prepare("LOGGING", "ACAB", _type=bool)
        use_acab_logging = self.value(spec)
        if not use_acab_logging:
            raise AcabConfigException("Logging is disabled")

        stream_fmt_spec   = self.prepare("LOGGING", "STREAM_FORMAT")
        file_fmt_spec     = self.prepare("LOGGING", "FILE_FORMAT")
        stream_level_spec = self.prepare("LOGGING", "STREAM_LEVEL")
        file_level_spec   = self.prepare("LOGGING", "FILE_LEVEL")

    except AcabConfigException:
        return

    # Acab Logging is go, use the full AcabLogRecord
    AcabLogRecord.install()

    logging.debug("Setting up Acab Log Formatting")
    stream_log_fmt = self.value(stream_fmt_spec)
    file_log_fmt   = self.value(file_fmt_spec)
    stream_level   = logmod._nameToLevel[self.value(stream_level_spec)]
    file_level     = logmod._nameToLevel[self.value(file_level_spec)]

    root_logger = logmod.getLogger()
    stream_handlers = [x for x in root_logger.handlers if not isinstance(x, logmod.FileHandler)]
    if bool(stream_handlers):
        stream_handlers[0].setFormatter(AcabLogFormatter(fmt=stream_log_fmt, record=True))
        stream_handlers[0].setLevel(max(0, stream_level))

    file_handlers = [x for x in root_logger.handlers if isinstance(x, logmod.FileHandler)]
    if bool(file_handlers):
        file_handlers[0].setFormatter(AcabNameTruncateFormatter(fmt=file_log_fmt))
        file_handlers[0].setLevel(max(0, file_level))
