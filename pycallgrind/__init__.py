from __future__ import absolute_import, print_function, division

from functools import wraps

from ._wrapper import lib

try:
    from ._numba import _wrap_numba
except ImportError:
    def _wrap_numba(func, tag=None):
        raise TypeError()

start_instrumentation = lib.start_instrumentation
stop_instrumentation = lib.stop_instrumentation
dump_stats = lib.dump_stats
dump_stats_at = lib.dump_stats_at
zero_stats = lib.zero_stats
toggle_collect = lib.toggle_collect


class callgrind(object):
    """Profiling with callgrind.

    A class for activating callgrind profiling only within certain contexts.

    Parameters
    ----------
    tag : str, optional
        If provided, callgrind output from the enclosed context will be tagged
        with this string.

    Examples
    --------

    Can be used as a contextmanager. Callgrind instrumentation will be
    activated only within this block, and will be dumped to file at the end of
    the block.

    >>> with callgrind(tag="foo"):
    ...     some_function()
    ...     another_function()

    Can also be used as a decorator. Instrumentation is only active during the
    function call.

    >>> @callgrind(tag="foo")
    ... def foo(a, b, c):
    ...     some_function()
    ...     another_function()

    If the decorated function is a numba jitted function, the result will also
    be a numba jitted function. This works in nopython mode as well.

    >>> @callgrind(tag="foo")
    ... @nb.njit
    ... def bar(a, b):
    ...     return a + b
    """

    def __new__(cls, tag=None):
        if callable(tag):
            return cls._wrap_function(tag)
        elif not isinstance(tag, (str, bytes)):
            raise TypeError("tag must be str, got {0}".format(type(tag)))
        obj = object.__new__(cls)

        if isinstance(tag, str):
            tag = tag.encode('ascii')

        obj.tag = tag
        return obj

    def __enter__(self):
        self.zero_stats()
        self.start()

    def __exit__(self, typ, value, traceback):
        self.stop()
        self.dump_stats()

    def __call__(self, func):
        return self._wrap_function(func, tag=self.tag)

    def start(self):
        """Start callgrind instrumentation, if not already enabled."""
        start_instrumentation()

    def stop(self):
        """Stop callgrind instrumentation, if not already disabled"""
        stop_instrumentation()

    def toggle(self):
        """Toggle the callgrind collection state"""
        toggle_collect()

    def zero_stats(self):
        """Reset the profile counters to zero"""
        zero_stats()

    def dump_stats(self):
        """Dump profiling stats. Written counters will be reset to zero"""
        dump_stats() if self.tag is None else dump_stats_at(self.tag)

    @staticmethod
    def _wrap_function(func, tag=None):
        if not (tag is None or isinstance(tag, str)):
            raise TypeError("tag must be str, got {0}".format(type(tag)))
        try:
            inner = _wrap_numba(func, tag=tag)
        except TypeError:

            @wraps(func)
            def inner(*args, **kwargs):
                with callgrind(tag):
                    return func(*args, **kwargs)

        return inner
