import os

from setuptools import setup


def read(fname):
    return open(
        os.path.join(
            os.path.dirname(__file__), fname)
        ).read()


setup(
    name='cachelock',
    license='MIT',
    version='0.0.1',
    python_requires='>=3.6',
    url='https://github.com/douglasfarinelli/python-cachelock',
    author='Douglas Farinelli',
    author_email='douglas.farinelli@gmail.com',
    keywords='lock cache once celery tasks single-execution',
    description='A simple look that uses the cache as acquirer',
    long_description=read('README.md'),
    py_modules=['cachelock'],
    platforms='any',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
