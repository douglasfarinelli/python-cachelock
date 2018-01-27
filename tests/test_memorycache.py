import inspect

import pytest

import cachelock


@pytest.fixture
def cache():
    return cachelock.MemoryCache()


def test_memorycache_should_be_a_class():
    assert inspect.isclass(cachelock.MemoryCache)


def test_memorycache_should_have_get_method():
    assert hasattr(cachelock.MemoryCache, 'get')


def test_memorycache_should_have_delete_method():
    assert hasattr(cachelock.MemoryCache, 'delete')


def test_memorycache_should_have_set_method():
    assert hasattr(cachelock.MemoryCache, 'set')


def test_memorycache_should_set_and_get_foo_key(cache):
    cache.set('foo', 1)
    assert cache.get('foo') is 1


def test_memorycache_should_delete_foo_key(cache):
    cache.set('foo', 1)
    cache.delete('foo')
    assert cache.get('foo') is None


def test_memorycache_should_return_none_for_nonexistent_key(cache):
    assert cache.get('foo') is None


def test_memorycache_should_internal_cache():
    cache_1 = cachelock.MemoryCache()
    cache_2 = cachelock.MemoryCache()
    assert cache_1 is not cache_2
    cache_1.set('foo', 1)
    cache_2.set('foo', 2)
    assert cache_1.get('foo') != cache_2.get('foo')
    cache_1.delete('foo')
    assert cache_2.get('foo') is 2
