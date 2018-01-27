from modulefinder import Module

import pytest

stub_cache = object()


class StubCacheHandler:

    def __getitem__(self, key):
        return stub_cache


@pytest.fixture(autouse=True)
def force_refresh_cachelock_from_modules():
    import sys
    del sys.modules['cachelock']


@pytest.fixture
def django():
    import sys
    try:
        django = sys.modules['django'] = Module(name='django')
        django.conf = sys.modules['django.conf'] = Module(name='django.conf')
        django.conf.settings = object()
        django.globalnames['conf'] = django.conf
        django.core = sys.modules['django.core'] = Module(name='django.core')
        django.globalnames['core'] = django.conf
        django.core.cache = Module(name='django.core.cache')
        sys.modules['django.core.cache'] = django.core.cache
        django.core.globalnames['cache'] = django.core.cache
        django.core.cache.cache = StubCacheHandler()
        yield
    finally:
        del sys.modules['django']
        del sys.modules['django.conf']
        del sys.modules['django.core']
        del sys.modules['django.core.cache']


def test_default_cache_should_be_django_cache_if_django_is_installed(django):
    import cachelock
    assert cachelock.default_cache is stub_cache


def test_default_cache_should_be_memory_cache_instance_if_not_django_installed(
):
    import cachelock
    assert isinstance(cachelock.default_cache, cachelock.MemoryCache)
