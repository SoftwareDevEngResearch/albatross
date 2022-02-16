# albatross

![example workflow](https://github.com/SoftwareDevEngResearch/albatross/actions/workflows/albatross.yml/badge.svg)

> A wind resource data retrieval, visualization, and analysis toolkit.

`albatross` is a Python package designed for wind energy analysis and visualization. It utilizes NREL's [Wind Integration National Dataset (WIND) Toolkit](https://www.nrel.gov/grid/wind-toolkit.html) and [REsource eXtraction (rex)](https://github.com/NREL/rex) package, and is inspired in part by a similar package aimed instead at Marine Renewable Energy, [MHKiT](https://github.com/MHKiT-Software/MHKiT-Python).

### Documentation

Documentation is hosted at [Read the Docs](https://albatross-wind.readthedocs.io).

To build the documentation locally, run the following after installing dependencies:

```bash
cd docs
make html
```

Afterwards, open \_build/index.html in a browser.

### Installation

`albatross` has not yet been hosted on PyPI, so for now, install from Github:

`pip install git+https://github.com/camirmas/albatross`

### Usage

After installation, run Jupyter notebook `Usage.ipynb` for examples.
