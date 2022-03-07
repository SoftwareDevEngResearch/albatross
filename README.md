# albatross 🐦

![example workflow](https://github.com/SoftwareDevEngResearch/albatross/actions/workflows/albatross.yml/badge.svg)

> A wind resource data retrieval, visualization, and analysis toolkit.

`albatross` is a Python package designed for wind energy analysis and visualization. It utilizes NREL's [Wind Integration National Dataset (WIND) Toolkit](https://www.nrel.gov/grid/wind-toolkit.html) and [REsource eXtraction (rex)](https://github.com/NREL/rex) package, and is inspired in part by a similar package aimed instead at Marine Renewable Energy, [MHKiT](https://github.com/MHKiT-Software/MHKiT-Python).

### Features

`albatross` consists of two primary modules:
- `requests`:
  - Request WIND Toolkit data by lat/lon point via HSDS
  - Read WIND Toolkit data from a local HDF5 file
  - Identify WIND Toolkit region and associated lat/lon coordinates, given a lat/lon point
- `analysis`:
  - Draw boxplots for inferred windspeed fields (or other specified fields)
  - Plot windrose chart for wind speed and direction data
  - Fit a Weibull distribution for wind speed data and plot a histogram/line chart showing probability density
  - Generate and/or plot diurnal statistics for wind speed data
  - Determine turbulence standard deviation using the Normal Turbulence model for wind data and a set of archetype wind turbine configurations

Future enhancements:
- multi-year requests
- allow use of CSV for `analysis` module functions
- further incorporate turbulence model statistics

### Documentation

Documentation is hosted at [Read the Docs](https://albatross-wind.readthedocs.io).

To build the documentation locally, run the following after installing [development](https://github.com/camirmas/albatross/edit/main/README.md#development) dependencies:

```bash
cd docs
make html
```

Afterwards, open \_build/index.html in a browser.

### Installation

`albatross` has not yet been hosted on PyPI, so for now, install from Github:

`pip install git+https://github.com/camirmas/albatross`

If you'll be using the `requests` module, you'll also need to [configure HSDS](https://github.com/NREL/hsds-examples#how-to-use).

### Usage

After installation, run Jupyter notebook `Usage.ipynb` for fully detailed examples.

### Development

For development, simply clone the repository, install dependencies, and run tests.

```bash
git clone git@github.com:camirmas/albatross.git
pip install -r requirements.txt
pytest
```
