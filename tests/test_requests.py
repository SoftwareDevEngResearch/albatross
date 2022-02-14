import os

import pytest
from pandas import DataFrame

from albatross import TESTDATADIR
from albatross.requests import (request_wtk_point_data, get_regions,
                                build_wtk_filepath, read_wtk_point_data,
                                identify_regions)

from albatross.utils import _load_wtk


lat_lon = (39.913561, -105.222422)
params = ['windspeed_90m']


# Test `identify_regions` #


def test_identify_regions_invalid_lat_lon():
    """Test invalid `lat_lon` inputs for `identify_regions`."""
    # wrong type
    lat_lon = 'bad'

    with pytest.raises(AssertionError) as e:
        identify_regions(lat_lon)

    msg = 'lat_lon must be a tuple or list'
    assert str(e.value) == msg

    # wrong element type
    lat_lon = ['bad']

    with pytest.raises(AssertionError) as e:
        identify_regions(lat_lon)

    msg = 'lat/lon points must be floats'
    assert str(e.value) == msg

    # wrong number of elements
    lat_lon = [1.0]

    with pytest.raises(AssertionError) as e:
        identify_regions(lat_lon)

    msg = 'lat_lon must have a length of 2'
    assert str(e.value) == msg

    # doesn't exist in datasets
    lat_lon = [1000.0, 1000.0]

    with pytest.raises(ValueError) as e:
        identify_regions(lat_lon)

    msg = 'No region found for specified lat/lon point.'
    assert str(e.value) == msg


def test_identify_regions():
    """Test valid inputs for `identify_regions`."""
    assert identify_regions(lat_lon) == ['conus']
    assert identify_regions((49.3556, -65.7146)) == ['canada', 'conus']

    wtk = _load_wtk()

    for region in wtk:
        lat_range, lon_range = wtk[region]['lat_lon_range']

        # lower
        assert region in identify_regions((lat_range[0], lon_range[0]))

        # upper
        assert region in identify_regions((lat_range[1], lon_range[1]))

        # middle
        mid_lat = (lat_range[0]+lat_range[0])/2
        mid_lon = (lon_range[0]+lon_range[0])/2
        assert region in identify_regions((mid_lat, mid_lon))


# Test `build_wtk_filepath` #


def test_build_wtk_filepath():
    """Test valid inputs for `build_wtk_filepath`."""

    # regular region
    res = build_wtk_filepath('conus', 2007)
    assert res == '/nrel/wtk/conus/wtk_conus_2007.h5'

    # region with alternate naming
    res = build_wtk_filepath('hawaii', 2007)
    assert res == '/nrel/wtk/hawaii/Hawaii_2007.h5'


def test_build_wtk_filepath_invalid_regions():
    """Test invalid `region` inputs for `build_wtk_filepath`."""
    with pytest.raises(AssertionError) as e:
        build_wtk_filepath('namek', 2007)
    assert str(e.value) == 'region not found: namek'


def test_build_wtk_filepath_years():
    """Test valid `year` inputs for `build_wtk_filepath`."""
    # beginning of year range
    res = build_wtk_filepath('canada', 2007)
    assert res == '/nrel/wtk/canada/wtk_canada_2007.h5'

    # end of year range
    res = build_wtk_filepath('canada', 2014)
    assert res == '/nrel/wtk/canada/wtk_canada_2014.h5'

    # between year range
    res = build_wtk_filepath('canada', 2010)
    assert res == '/nrel/wtk/canada/wtk_canada_2010.h5'


def test_build_wtk_filepath_invalid_year():
    """Test invalid `year` inputs for `build_wtk_filepath`."""
    with pytest.raises(AssertionError) as e:
        build_wtk_filepath('canada', 2015)

    msg = 'year %s not available for region: %s' % (2015, 'canada')
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        build_wtk_filepath('canada', '2015')

    msg = '"year" must be an integer'
    assert str(e.value) == msg


def test_build_wtk_filepath_resolutions():
    """Test valid `resolution` inputs for `build_wtk_filepath`."""
    # no input defaults to "hourly"
    res = build_wtk_filepath('mexico', 2010)
    assert res == '/nrel/wtk/mexico/wtk_mexico_2010.h5'

    # "hourly" can be explicitly specified
    res = build_wtk_filepath('mexico', 2010, resolution='hourly')
    assert res == '/nrel/wtk/mexico/wtk_mexico_2010.h5'

    # "5min"
    res = build_wtk_filepath('mexico', 2010, resolution='5min')
    assert res == '/nrel/wtk/mexico-5min/wtk_mexico_2010.h5'


def test_build_wtk_filepath_invalid_resolution():
    """Test valid `resolution` inputs for `build_wtk_filepath`."""
    with pytest.raises(AssertionError) as e:
        build_wtk_filepath('canada', 2010, resolution='1min')

    msg = 'resolution "%s" not available for region: %s' % (
        '1min', 'canada')
    assert str(e.value) == msg


# Test `get_regions` #


def test_get_regions():
    """Simply test `get_regions`."""
    wtk = _load_wtk()
    assert get_regions() == wtk


# Test `request_wtk_point_data` #


def test_request_wtk_point_data_invalid_lat_lon():
    """Test invalid `lat_lon` inputs for `request_wtk_point_data`."""
    # wrong type
    lat_lon = 'bad'

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(lat_lon, 2010, params, resolution='5min')

    msg = 'lat_lon must be a tuple or list'
    assert str(e.value) == msg

    # wrong element type
    lat_lon = ['bad']

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(lat_lon, 2010, params, resolution='5min')

    msg = 'lat/lon points must be floats'
    assert str(e.value) == msg

    # wrong number of elements
    lat_lon = [1.0]

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(lat_lon, 2010, params, resolution='5min')

    msg = 'lat_lon must have a length of 2'
    assert str(e.value) == msg


def test_request_wtk_point_data_invalid_params():
    """Test invalid `params` inputs for `request_wtk_point_data`."""
    # wrong type
    params = 'bad'

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(lat_lon, 2010, params, resolution='5min')

    msg = '"params" must be a tuple or list'
    assert str(e.value) == msg

    # empty params
    params = []

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(lat_lon, 2010, params, resolution='5min')

    msg = '"params" must not be empty'
    assert str(e.value) == msg

    # wrong param type
    params = [1]

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(lat_lon, 2010, params, resolution='5min')

    msg = '"params" elements must be strings'
    assert str(e.value) == msg


def test_request_wtk_point_data_multi_region():
    """
    Test that `request_wtk_point_data` requires user to explicitly specify `region`
    if `identify_region` returns multiply regions.
    """
    lat_lon = (49.3556, -65.7146)

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(lat_lon, 2010, params, resolution='5min')

    msg = (
        'Multiple regions identified for the given lat/lon point: %s.\n'
        'Please specify one using the `region` arg.'
    ) % (['canada', 'conus'],)
    assert str(e.value) == msg


# Test `read_wtk_point_data` #


def test_read_wtk_point_data_invalid_lat_lon():
    """Test invalid `lat_lon` inputs for `read_wtk_point_data`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    # wrong type
    lat_lon = 'bad'

    with pytest.raises(AssertionError) as e:
        read_wtk_point_data(path, lat_lon, params)

    msg = 'lat_lon must be a tuple or list'
    assert str(e.value) == msg

    # wrong element type
    lat_lon = ['bad']

    with pytest.raises(AssertionError) as e:
        read_wtk_point_data(path, lat_lon, params)

    msg = 'lat/lon points must be floats'
    assert str(e.value) == msg

    # wrong number of elements
    lat_lon = [1.0]

    with pytest.raises(AssertionError) as e:
        read_wtk_point_data(path, lat_lon, params)

    msg = 'lat_lon must have a length of 2'
    assert str(e.value) == msg


def test_read_wtk_point_data_invalid_params():
    """Test invalid `params` inputs for `read_wtk_point_data`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    # wrong type
    params = 'bad'

    with pytest.raises(AssertionError) as e:
        read_wtk_point_data(path, lat_lon, params)

    msg = '"params" must be a tuple or list'
    assert str(e.value) == msg

    # empty params
    params = []

    with pytest.raises(AssertionError) as e:
        read_wtk_point_data(path, lat_lon, params)

    msg = '"params" must not be empty'
    assert str(e.value) == msg

    # wrong param type
    params = [1]

    with pytest.raises(AssertionError) as e:
        read_wtk_point_data(path, lat_lon, params)

    msg = '"params" elements must be strings'
    assert str(e.value) == msg


def test_read_wtk_point_data():
    """Tests `read_wtk_point_data`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    data, meta = read_wtk_point_data(path, lat_lon, ['windspeed_100m'])

    assert type(data) == DataFrame
    assert type(meta) == DataFrame

    assert len(data) == 8784
    assert len(data.columns) == 1
    assert data.columns[:] == ['windspeed_100m']
    assert data.loc['2012-01-01 00:00:00']['windspeed_100m'] == 7.25
    assert len(meta) == 200
    assert len(meta.columns[:]) == 8
