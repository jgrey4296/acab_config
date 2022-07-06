from __future__ import annotations

import abc
import logging as logmod
import unittest
import warnings
from dataclasses import InitVar, dataclass, field
from importlib.resources import files
from os.path import join, split, splitext
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)

from acab_config.config import AcabConfig, ConfigSpec
from acab_config.config_meta import ConfigSingletonMeta
from acab_config.error.config_error import AcabConfigException
from acab_config.hooks.misc_hooks import attr_hook
from acab_config.utils.log_formatter import AcabMinimalLogRecord

if TYPE_CHECKING:
    # tc only imports
    pass

logging = logmod.getLogger(__name__)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    AcabMinimalLogRecord.install()

class ConfigOverrideTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LOGLEVEL      = logmod.DEBUG
        LOG_FILE_NAME = "log.{}".format(splitext(split(__file__)[1])[0])
        cls.file_h        = logmod.FileHandler(LOG_FILE_NAME, mode="w")

        cls.file_h.setLevel(LOGLEVEL)
        logging = logmod.getLogger(__name__)
        logging.root.setLevel(logmod.NOTSET)
        logging.root.addHandler(cls.file_h)
        logging.root.handlers[0].setLevel(logmod.WARNING)

        cls.base = files("acab_config.__tests")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            AcabConfig(reset=True)

    @classmethod
    def tearDownClass(cls):
        logmod.root.removeHandler(cls.file_h)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            AcabConfig(reset=True)

    def setUp(self):
        data_path   = files("acab_config.__tests")
        base_config = data_path.joinpath("basic.config")
        self.config = AcabConfig(base_config, build=True)

    def tearDown(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.config = AcabConfig(reset=True)

    def test_clear(self):
        spec = self.config.prepare("Handler.System", "DEFAULT_SIGNAL")
        self.assertIsInstance(spec, ConfigSpec)
        self.assertEqual(spec(), "test")
        self.config.clear()
        self.assertFalse(bool(self.config))
        with self.assertRaises(AcabConfigException):
            self.config.prepare("Handler.System", "DEFAULT_SIGNAL")

    def test_clear_attr(self):
        AcabConfig(hooks=[attr_hook]).run_hooks()
        self.assertEqual(self.config.attr.Handler.System.DEFAULT_SIGNAL, "test")
        self.config.clear()
        self.assertFalse(bool(self.config))
        self.assertFalse(self.config.attr)
        with self.assertRaises(AttributeError):
            self.config.attr.Handler.System.DEFAULT_SIGNAL

    def test_clear_hooks(self):
        AcabConfig(hooks=[lambda x: x])
        self.assertTrue(self.config.hooks)
        AcabConfig(hooks=False)
        self.config.clear()
        self.assertFalse(self.config.hooks)

    def test_override(self):
        spec = self.config.prepare("Handler.System", "DEFAULT_SIGNAL")
        with self.assertWarns(UserWarning):
            self.assertIsInstance(spec, ConfigSpec)
            self.assertEqual(spec(), "test")
            self.config.read([join(self.base, "override.config")])
            self.assertIsInstance(spec, ConfigSpec)
            self.assertEqual(spec(), "blah")

    def test_warn_on_override(self):
        self.config.specs_invalid = {}
        spec = self.config.prepare("Handler.System", "DEFAULT_SIGNAL")
        val = spec()
        with self.assertWarns(UserWarning):
            self.config.read([join(self.base, "override.config")])
            val2 = spec()

    def test_silent_override(self):
        """
        Overrides silently when the spec isn't called before the override
        """
        self.config.specs_invalid = {}
        spec = self.config.prepare("Handler.System", "DEFAULT_SIGNAL")
        self.config.read([join(self.base, "override.config")])
        val = spec()

    def test_attr_override(self):
        AcabConfig(hooks=[attr_hook]).run_hooks()
        val = self.config.attr.Handler.System.DEFAULT_SIGNAL
        self.assertEqual(val, "test")
        self.config.read([join(self.base, "override.config")])
        self.assertEqual(self.config.attr.Handler.System.DEFAULT_SIGNAL, "blah")

    def test_programmatic_override(self):
        spec = self.config.prepare("Handler.System", "DEFAULT_SIGNAL")
        self.assertIsInstance(spec, ConfigSpec)
        self.assertEqual(spec(), "test")
        self.config.override(spec, "blah")
        self.assertEqual(spec(), "blah")




    def test_spec_non_equality(self):
        spec1 = self.config.prepare("Handler.System", "DEFAULT_SIGNAL")
        spec2 = self.config.prepare("Handler.System", "OTHER")
        self.assertNotEqual(spec1, spec2)

    def test_spec_non_duplication(self):
        spec1 = self.config.prepare("Handler.System", "DEFAULT_SIGNAL")
        spec2 = self.config.prepare("Handler.System", "DEFAULT_SIGNAL", _type=bool)
        self.assertEqual(spec1, spec2)
        self.assertIsNot(spec1, spec2)

