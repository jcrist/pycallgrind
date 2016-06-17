## Pycallgrind

Utilities for context based profiling with
[callgrind](http://valgrind.org/docs/manual/cl-manual.html). This is backed by
[CFFI](http://cffi.readthedocs.io/en/latest/) based wrappers for callgrind's
[client
requests](http://valgrind.org/docs/manual/cl-manual.html#cl-manual.clientrequests).

## Usage

The main api entry point is ``pycallgrind.callgrind``. This can be used as a
contextmanager. Callgrind instrumentation will be activated only within this
block, and will be dumped to file at the end of the block.

```python
>>> from pycallgrind import callgrind
>>> with callgrind(tag="foo"):
...     some_function()
...     another_function()
```

It can also be used as a decorator. Instrumentation is only active during the
function call.

```python
>>> @callgrind(tag="foo")
... def foo(a, b, c):
...     some_function()
...     another_function()
```

If the decorated function is a numba jitted function, the result will also
be a numba jitted function. This works in nopython mode as well.

```python
>>> @callgrind(tag="foo")
... @nb.njit
... def bar(a, b):
...     return a + b
```

The lower level client request functions are also included. These are trivial
wrappers around the callgrind macros of the same name.

Note: Since instrumentation will be turned on during code execution, you
probably want to include the ``--instr-atstart=no`` flag:

```bash
valgrind --tool=callgrind --instr-atstart=no python myfile.py
```
