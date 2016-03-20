kfreader-cffi
===================

.. image:: https://travis-ci.org/mstolyarchuk/kfreader-cffi.svg?branch=master
    :target: https://travis-ci.org/mstolyarchuk/kfreader-cffi

kfreader-cffi is a Python package for reading binary result files produced by
the Amsterdam Density Functional (ADF) program suite (http://scm.com). Instead of kf.py_, this package does not require working ADF installation.

It uses CFFI_ to interface with the original C library KFReader_.

Installation
------------

*Note that kfreader-cffi currently is only tested under Python 3.x on Ubuntu*

First we need to install some prerequisites:

.. code:: sh

  apt-get update
  apt-get install build-essential gcc libffi-dev python3-dev

Then to install the package, simply:

.. code:: sh

  pip install kfreader-cffi
  
Or for development:

.. code:: sh
  
  git clone https://github.com/mstolyarchuk/kfreader-cffi
  pip install -e kfreader-cffi

Shared library ``libkfreader.so`` will be *automatically* built from C source files
provided in /vendor directory during the installation process
(see ``Makefile`` for details).
  
Now you are ready to go!

Getting started
---------------

Before attempting to use this package, you might find the official
documentation_ on TAPE21 useful.

Usage
^^^^^

.. code:: python

	>>> from kfreader import KFReader, kfropen
	
	# Open a TAPE21 file.
	>>> kfr = KFReader('file.t21')
	# Get the value of a variable given its section and name.
	>>> kfr.get_data('General', 'file-ident')
	'TAPE21'
	>>> kfr.close()
	
	# We can also seamlessly use the with-statement.
	# Let's simplify the above example:
	>>> with kfropen('file.t21') as kfr:
	>>>	# Use the reader as regular. The file will be closed
	>>>     # when the block ends.
	>>>     print(kfr.get_data('General', 'termination status'))
	'NORMAL TERMINATION'

Acknowledgments
---------------

Many thanks to Alexei Yakovlev and all the other developers (http://scm.com) of the original C routines.
This package would not exist without their work.

.. _kf.py: http://www.scm.com/Downloads/2014/
.. _CFFI: https://cffi.readthedocs.org/
.. _KFReader: http://www.scm.com/Downloads/2014/
.. _documentation: https://www.scm.com/documentation/ADF/Appendices/TAPE21/
