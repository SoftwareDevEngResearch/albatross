import pytest
from albatross.requests import request_wtk_point_data, get_regions, build_wtk_filepath
from albatross.utils import _load_wtk


lat_lon = (39.913561, -105.222422)
params = ['windspeed_90m']


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


def test_get_regions():
    """Simply test `get_regions`."""
    wtk = _load_wtk()
    assert get_regions() == wtk


def test_request_wtk_point_data_invalid_lat_lon():
    # wrong type
    lat_lon = 'bad'

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(
            'canada', 2010, lat_lon, params, resolution='5min')

    msg = 'lat_lon must be a tuple or list'
    assert str(e.value) == msg

    # wrong element type
    lat_lon = ['bad']

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(
            'canada', 2010, lat_lon, params, resolution='5min')

    msg = 'lat/lon points must be floats'
    assert str(e.value) == msg

    # wrong number of elements
    lat_lon = [1.0]

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(
            'canada', 2010, lat_lon, params, resolution='5min')

    msg = 'lat_lon must have a length of 2'
    assert str(e.value) == msg


def test_request_wtk_point_data_invalid_params():
    """Test invalid `params` inputs for `request_wtk_point_data`"""
    # wrong type
    params = 'bad'

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(
            'canada', 2010, lat_lon, params, resolution='5min')

    msg = '"params" must be a tuple or list'
    assert str(e.value) == msg

    # empty params
    params = []

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(
            'canada', 2010, lat_lon, params, resolution='5min')

    msg = '"params" must not be empty'
    assert str(e.value) == msg

    # wrong param type
    params = [1]

    with pytest.raises(AssertionError) as e:
        request_wtk_point_data(
            'canada', 2010, lat_lon, params, resolution='5min')

    msg = '"params" elements must be strings'
    assert str(e.value) == msg
