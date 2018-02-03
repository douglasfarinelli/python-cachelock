python-cachelock
================

[![Supported Versions](https://img.shields.io/pypi/pyversions/cachelock.svg)](https://pypi.python.org/pypi/cachelock)
[![Build Status](https://travis-ci.org/douglasfarinelli/python-cachelock.svg?branch=master)](https://travis-ci.org/douglasfarinelli/python-cachelock)
[![Coverage Status](https://coveralls.io/repos/github/douglasfarinelli/python-cachelock/badge.svg?branch=master)](https://coveralls.io/github/douglasfarinelli/python-cachelock?branch=master)
[![PyPI version](https://badge.fury.io/py/cachelock.svg)](https://pypi.python.org/pypi/cachelock)

The `cachelock` serves to ensure that your code block or function is executed one at a time using the cache as acquirer.

How to install:
===============

    pip install cachelock

or

    pipenv install cachelock
    
How to use
==========

You can use of two forms:

    - Use the `Lock` class to your blocks;
    - Or use the decorator `once` to block your functions or tasks;

With cachelock.Lock
===================

Arguments:

    with cachelock.Lock(
        key=...
        cache=...,
    ) ...

You should use the Lock class as with context:

    with cachelock.Lock(key='foo'):
        ...your code ...

If it is already locked, the LockError will be raised.

With cachelock.once
===================

Arguments:

    @cachelock.once(
        key=...
        cache=...,
        raises_if_lock=False
    )
    ...

With the decorator, you can guarantee the unique execution of some function. It also allows you to configure your key according to the arguments of the function.

    @celery.task
    @cachelock.once(key='foo-{arg_a}-{arg_b}')
    def func(arg_a, arg_b):
        pass

That way, if it is locked, the function quits silently. You can also ask `once` to raise `LockError`:

    @celery.task
    @cachelock.once(
        key='foo-{arg_a}-{arg_b}',
        raise_if_lock=True
    )
    def func(arg_a, arg_b):
        pass

Integrate with Django
=====================

The cachelock checks whether django is installed, and if so, it uses django's own cache as aquirer. And if you wish, you can modify the default cache with `DEFAULT_CACHELOCK_ALIAS` configuration through django settings. The value must be an alias of some existing cache, by default it uses `default`


*Remembering that by `default`, `cachelock` uses its own internal cache in memory if there is no integration with `django`.*

Customizing your own cache
==========================

To work it is necessary that the implementation of the cache has the `get`, `delete` and `set` methods. Ex.:

    class DummyCache:

        def set(self, key, value):
            pass

        def get(self, key, default=None):
            pass

        def delete(self, key):
            pass

    cache = DummyCache()

use: 

    @cachelock.once(key=..., cache=cache)
    
or
    
    with cachelock.Lock(key..., cache=cache) ...
    