import subprocess
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py


build_msg = "Building shared library libkfreader.so"

def post_hook():
    import os
    subprocess.check_call(['make', 'libkfreader.so'])


class install_command(install):
    def run(self):
        self.execute(post_hook, [], build_msg)
        install.run(self)


class develop_command(develop):
    def run(self):
        self.execute(post_hook, [], build_msg)
        develop.run(self)


class build_py_command(build_py):
    def run(self):
        self.execute(post_hook, [], build_msg)
        build_py.run(self)


setup(
    cmdclass={
        'install': install_command,
        'develop': develop_command,
        'build_py': build_py_command
    },
    name='kfreader-cffi',
    version='0.2.4',
    url='https://github.com/mstolyarchuk/kfreader-cffi',
    author='Maxim Stolyarchuk',
    author_email='maxim.stolyarchuk@gmail.com',
    description='Python bindings for KFReader, a library from the ADF computational chemistry package',
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    packages=['kfreader'],
    package_data={'kfreader': ['vendor/libkfreader.so']},
    install_requires=['cffi'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
