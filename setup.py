import subprocess
from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop


build_msg = "Building shared library libkfreader.so"

def post_hook():
    subprocess.call(['make', 'libkfreader.so'])


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(post_hook, [], build_msg)


class develop(_develop):
    def run(self):
        _develop.run(self)
        self.execute(post_hook, [], build_msg)


setup(
    cmdclass={
        'install': install,
        'develop': develop
    },
    name='kffreader-cffi',
    version='0.2.0',
    url='https://github.com/mstolyarchuk/kfreader-cffi',
    author='Maxim Stolyarchuk',
    author_email='maxim.stolyarchuk@gmail.com',
    description='Python bindings for KFReader, a library from the ADF computational chemistry package',
    long_description=__doc__,
    py_modules=['kfreader'],
    zip_safe=False,
    include_package_data=True,
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
