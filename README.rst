kfreader-cffi
===================

It uses cffi_ to interface with the original C library KFReader_.

Installation
------------

*Note that kfreader-cffi currently is only tested under Python3.\* on Ubuntu*

First we need to install some prerequisites

.. code:: sh

  sudo apt-get update
  sudo apt-get install gcc make cmake python3-dev libffi-dev

Then to install the package, simply

.. code:: sh

  pip install kfreader-cffi
  
Or for development

.. code:: sh
  
  git clone https://github.com/mstolyarchuk/kfreader-cffi
  pip install -e kfreader-cffi

Shared library ``libkfreader.so`` will be *automatically* built from C source files
provided in /lib directory during the installation process
(see ``Makefile`` for details).
  
Now you are ready to go!

Getting started
---------------

Before attempting to use this package, you might find the official
documentation_ on TAPE21 useful.

Usage
^^^^^

.. code:: python

	>>> from kfreader import KFReader
	
	>>> kfr = KFReader('file.t21')
	>>> kfr.get_data('General', 'termination status')
	'NORMAL TERMINATION'
	
	>>> kfr.close()

Acknowledgments
---------------

Many thanks to Alexei Yakovlev and other SCM developers for their work on the original C routines.
This package would not exist without their work.

.. _cffi: https://cffi.readthedocs.org/
.. _KFReader: http://www.scm.com/Downloads/2014/
.. _documentation: http://www.scm.com/Doc/Doc2014/ADF/ADFUsersGuide/page334.html
