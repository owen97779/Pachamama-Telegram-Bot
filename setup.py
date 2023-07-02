try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='telegrambot',
      use_scm_version=True,
        setup_requires=['setuptools_scm'],
        version='1.0',
        description='Python Telegram Bot',
        author='Benji / Owen97779',
        packages=['telegrambot'])
