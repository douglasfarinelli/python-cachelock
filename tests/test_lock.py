import contextlib
import inspect
from unittest.mock import patch

import pytest

import cachelock


def test_lock_should_be_class_instance():
    assert inspect.isclass(cachelock.Lock)


def test_lock_should_raises_lock_error():
    try:
        cachelock.default_cache.set('foo', 1)
        with pytest.raises(cachelock.LockError):
            with cachelock.Lock(key='foo'):
                pass
    finally:
        cachelock.default_cache.delete(key='foo')


def test_lock_should_not_raises_lock_error():
    with cachelock.Lock(key='foo'):
        pass


def test_lock_should_calls_for_cache_methods():
    lock = cachelock.Lock(key='foo')

    with patch.object(lock, 'cache') as cache:
        cache.get.return_value = None
        with lock:
            cache.get.assert_called_with('foo')
            cache.set.assert_called_with('foo', 1)
        cache.delete.assert_called_with('foo')

        cache.get.return_value = 1
        with contextlib.suppress(cachelock.LockError):
            with lock:
                assert cache.get.called
                assert not cache.set.called
            assert cache.delete.called
