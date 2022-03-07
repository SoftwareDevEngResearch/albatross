albatross
=========

``albatross`` is a Python package designed for wind energy analysis and visualization. It utilizes NREL's [Wind Integration National Dataset (WIND) Toolkit](https://www.nrel.gov/grid/wind-toolkit.html) and [REsource eXtraction (rex)](https://github.com/NREL/rex) package, and is inspired in part by a similar package aimed instead at Marine Renewable Energy, [MHKiT](https://github.com/MHKiT-Software/MHKiT-Python).

Features
--------

``albatross`` consists of two primary modules:

* ``requests``:

  * Request WIND Toolkit data by lat/lon point via HSDS
  * Read WIND Toolkit data from a local HDF5 file
  * Identify WIND Toolkit region and associated lat/lon coordinates, given a lat/lon point

* ``analysis``:

  * Draw boxplots for inferred windspeed fields (or other specified fields)
  * Plot windrose chart for wind speed and direction data
  * Fit a Weibull distribution for wind speed data and plot a histogram/line chart showing probability density
  * Generate and/or plot diurnal statistics for wind speed data
  * Determine turbulence standard deviation using the Normal Turbulence model for wind data and a set of archetype wind turbine configurations

Future enhancements:

* multi-year requests
* allow use of CSV for ``analysis`` module functions
* further incorporate turbulence model statistics

Contents
--------

.. toctree::

   modules

.. toctree::
   :maxdepth: 1

   installation
   proposal

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
