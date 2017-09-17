===============================
warren
===============================

Warren, an python module for extensible econometrics

* Free software: MIT license

Features
--------

* Data retrieval using Quandl https://www.quandl.com
* Financial statements comparison
* ARIMA time series modelling
* Linear regression modelling
* VAR modelling

Installation
--------

Directly from github using pip

.. highlight:: bash
pip install git+git://github.com/agounaris/warren

Building it locally

* Checkout the repository github.com/agounaris/warren
* Navigate under warren directory
* Build the package using the command python setup.py sdist
* Install the .tar.gz file using pip (pip install dist/warren-0.1.0.tar.gz)

Usage
--------

After installation execute the app by typing 'warren' on the
command line

Sample commands using the REPL

.. code-block:: python
    compare MSFT balance_sheet 2015 2016

.. code-block:: python
    arima 2015-11-11 2016-11-11 MSFT 1

.. code-block:: python
    ols 2015-11-11 2016-11-11 MSFT AAPL NDAQ

.. code-block:: python
    var 2015-11-11 2016-11-11 MSFT AAPL NDAQ

Under development
--------

* TODO

Credits
---------

This package was created as a final project for the MSc Computing for Financial Services programme

