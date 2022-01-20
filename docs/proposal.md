# Original Project Proposal

`albatross` is a Python package designed for wind energy analysis and visualization. It utilizes NREL's [Wind Integration National Dataset (WIND) Toolkit](https://www.nrel.gov/grid/wind-toolkit.html) and [REsource eXtraction (rex)](https://github.com/NREL/rex) package, and is inspired in part by a similar package aimed instead at Marine Renewable Energy, [MHKiT](https://github.com/MHKiT-Software/MHKiT-Python).

## Methodology

The primary goal for this project is to provide an accessible and extensible interface for retrieving and working with NREL's WIND Toolkit. NREL provides this information via its Highly Scalable Data Service (HSDS), an extensive and powerful database containing over 50TB of data. While `rex` assists with data retrieval, wind researchers and analysts will benefit from a streamlined interface for requesting and analyzing wind resource data. Ultimately, my intent is to build upon this package as I learn more about wind resource assessment methodologies through research and coursework.

While this project is not directly related to my current research, it will prove a valuable tool in the future, as I engage more fully in wind turbine design research. To this point, while some open-source wind resource analysis tools exist, I have not discovered any packages that work directly with HSDS WIND.  

## Features

### 1. Toolkit Integration

Much like the implementation seen in `MHKiT`, this package will wrap the functionality provided by HSDS and `rex` to provide an interface that simplifies data requests in a generalized manner. This step is more an exercise in user experience than computational science. In practice, this will likely appear as a `request` module with the following functionality:

#### Region identification 

Users should be able to identify the region for a given lat/lon point. This can be used to help formulate requests and to verify that lat/lon points are valid.

#### Wind dataset retrieval

Users should be able to request wind data with the following parameters:
- resource type
- lat/lon point(s)
- year(s)
- region(s)

_note: Additional exploration is needed to determine if other, less documented filtering options are available from HSDS._

Users should be able to request multiple datasets at a time, thought rate-limiting rules may apply, and rate-limiting errors should be handled appropriately.

Users should also be able to easily access local `.h5` files. While these files tend to be very large, it is possible that users are running their own servers, and wish to query data without concern for rate-limiting. This feature will likely require users to specify their own filepaths for flexibility reasons (there is no reason to be prescriptive about how the files should be stored on the user's local machine).

### 2. Analysis Tools

The `analysis` module will build upon the streamlined data retrieval process in Step 1, providing data analysis tools specific to existing wind resource assessment methodologies. The scope of this feature is difficult to define, as any number of techniques may benefit the analysis of wind resources; however, IEC standards exist for wind resource assessments, and will form the basis for the functionality in this module. I will use the following academic resources:

- IEC 61400-1
- IEC 61400-3-1
- IEC 61400-3-2
- Robertson B, Dunkle G, Gadasi J, Garcia-Medina G, Yang Z, Holistic Marine
Energy Resource Assessments: A Wave and Offshore Wind Perspective of Metocean Conditions,
Renewable Energy, https://doi.org/10.1016/j.renene.2021.01.136.

## Testing

### Unit Tests

#### `requests`

For local requests, unit tests will ensure that `.h5` files can be accessed via the local filesystem. For network requests, responses will need to be stubbed, as unit testing live network requests is a complicated and error prone process. For both scenarios, an `.h5` file will be provided within the testing package.

#### `analysis`

This module will be tested in a more straightforward manner. It will also utilize the `.h5` file provided within the testing package.

### Integration Tests

Integration tests will involve full playthroughs of existing features, emphasizing the connection between requesting data and analyzing it. These tests will use local `.h5` files, and will not perform any network requests.

## Documentation

Documentation will be auto-generated using [Read the Docs](https://docs.readthedocs.io). The package will also include example Jupyter notebooks.

## Publication

This package will utilize an MIT License, and will be hosted on [PyPI](https://pypi.org/)

## Dependencies

(This is a working list)

- `h5pyd`: configures access to HSDS servers
- `NREL-rex`: HSDS resource extraction
- `numpy`: data tools
- `pandas`: data tools
- `matplotlib`: visualization
- `pytest`: testing
- `ipdb`: debugging

