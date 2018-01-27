"""
Copyright (c) 2018 Douglas Farinelli

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import functools
import inspect
import logging

logger = logging.getLogger(__name__)


class LockError(Exception):
    pass


class MemoryCache:

    def __init__(self):
        self.__cache = {}

    def set(self, key, value):
        self.__cache[key] = value

    def get(self, key, default=None):
        return self.__cache.get(key, default)

    def delete(self, key):
        if key in self.__cache:
            del self.__cache[key]


try:
    from django.conf import settings
except ModuleNotFoundError:
    default_cache = MemoryCache()
else:
    from django.core.cache import cache
    default_cache = cache[getattr(
        settings,
        'DEFAULT_CACHELOCK_ALIAS',
        'default'
    )]


class Lock:
    """
    Context Manager that lets you run one at a time
    using cache as lock.

    How to use:

    with Lock(key='foo'):
         ...

    if locked:

    [out] LockError
    """

    def __init__(self, key, cache=None):
        """
        :param key: must be a string.
        :param cache: must be cache backend, with get, set and delete methods.
        """
        self.key = key
        self.cache = cache or default_cache

    def __enter__(self):
        cached = self.cache.get(self.key)
        if cached:
            logger.warning(
                f'Locked {self.key} is active. Trying again after release.'
            )
            raise LockError()
        self.cache.set(self.key, 1)
        logger.info(f'Created lock for {self.key}.')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cache.delete(self.key)
        logger.info(f'Released lock for {self.key}.')


def once(
    key,
    cache=default_cache,
    raise_if_lock=False
):
    """
    Decorator for execute function if not locked.

    :param key: must be a string and allow dynamic format.
    :param cache: must be cache backend, with get,
        set and delete methods.
    :param raise_if_lock: raise LockError if is active.

    How to use:

    @once(key='tracking-lock')
    def tracking(code):
        ...

    or with dynamic format key

    @celery.task
    @once(key='tracking-lock-by-{code}'
    def tracking(code):
        ...

    @once(key='tracking-lock-by-{code}-and-{order_id}')
    def tracking(code, order_id):
        ...

    @once(..., cache=..., raise_if_lock=True)
    def tracking(...):
        ...

    if locked:

    [out] LockError
    """
    def decorator(func):
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            try:
                try:
                    _key = key.format(**bound.arguments)
                except IndexError:
                    raise ValueError(
                        'Please, use named arguments to format your keys. '
                        'Ex.: "foo-{arg_a}..."'
                    )
                with Lock(key=_key, cache=cache):
                    return func(*args, **kwargs)
            except LockError:
                if raise_if_lock:
                    raise
        return wrapper

    return decorator
