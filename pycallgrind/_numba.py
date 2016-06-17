from __future__ import absolute_import, print_function, division

import numpy as np
import numba as nb
from numba.targets.registry import CPUDispatcher
from numba.cffi_support import register_module

from . import _wrapper
from ._wrapper import lib, ffi

register_module(_wrapper)

start_instrumentation = lib.start_instrumentation
stop_instrumentation = lib.stop_instrumentation
zero_stats = lib.zero_stats
dump_stats = lib.dump_stats
dump_stats_at = lib.dump_stats_at


def _wrap_numba(func, tag=None):
    if not isinstance(func, CPUDispatcher):
        raise TypeError("Not a numba dispatch function")

    if tag is None:

        @nb.jit(**func.targetoptions)
        def inner(*args):
            zero_stats()
            start_instrumentation()
            res = func(*args)
            stop_instrumentation()
            dump_stats()
            return res

    elif isinstance(tag, str):
        tag = np.array([ord(i) for i in tag], dtype='i1')

        @nb.jit(**func.targetoptions)
        def inner(*args):
            zero_stats()
            start_instrumentation()
            res = func(*args)
            stop_instrumentation()
            dump_stats_at(ffi.from_buffer(tag))
            return res
    else:
        raise TypeError("tag must be str, got {0}".format(type(tag)))
    return inner
