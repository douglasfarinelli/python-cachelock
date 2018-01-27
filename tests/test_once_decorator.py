import inspect
from unittest.mock import patch

import pytest

import cachelock


def test_once_should_a_function():
    assert inspect.isfunction(cachelock.once)


@pytest.mark.parametrize('args,key,formatted_key', [
    (('teste','foo'), 'foo-key-{arg_a}', 'foo-key-teste'),
    (('teste','foo'), 'foo-key-{arg_b}', 'foo-key-foo'),
    (('teste','foo'), 'foo-key-{arg_a}-{arg_b}', 'foo-key-teste-foo'),
])
def test_once_should_generate_key_from_signature(args, key, formatted_key):

    with patch.object(cachelock, 'Lock') as Lock:

        @cachelock.once(key=key)
        def func(arg_a, arg_b):
            pass

        func(*args)

        Lock.assert_called_with(
            key=formatted_key,
            cache=cachelock.default_cache
        )


def test_once_should_raises_value_error_if_not_named_key():
    with pytest.raises(ValueError):

        @cachelock.once(key='foo-key-{0}')
        def func(arg_a, arg_b):
            pass

        func(1, 2)

        func(arg_a=1, arg_b=2)


def test_once_should_raises_lock_error_if_param_is_true():
    try:
        cachelock.default_cache.set('foo', 1)

        with pytest.raises(cachelock.LockError):

            @cachelock.once(
                key='foo',
                raise_if_lock=True
            )
            def func(arg_a, arg_b):
                pass

            func(1, 2)
    finally:
        cachelock.default_cache.delete('foo')
