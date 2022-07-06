#!/usr/bin/env python3
from __future__ import annotations

import abc
import logging as logmod
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from re import Pattern
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1
from weakref import ref

logging = logmod.getLogger(__name__)

if TYPE_CHECKING:
    # tc only imports
    pass

def mapToEnum(the_dict:dict[Enum, Any], enum_v:Enum) -> Callable[..., Any]:
    """
    Utility decorator to simplify creating a mapping of enum entries to
    functions.
    """
    def wrapper(fn):
        the_dict[enum_v] = fn
        return fn

    return wrapper

def registerOn(cls:type) -> Callable[..., Any]:
    """ Decorator for registering a function onto a class as a method """
    def wrapper(fn):
        logging.info(f"Method Registration: {cls.__name__} . {fn.__name__}")
        assert(fn.__name__ not in dir(cls))
        setattr(cls, fn.__name__, fn) #type:ignore
        return fn

    return wrapper
