import pytest
from albatross.requests import request_wind_data


def test_request_wind_data_regions():
    """Test valid region inputs for `request_wind_data`."""
    # regular region
    res = request_wind_data('conus', 2007)
    assert res == '/nrel/wtk/conus/wtk_conus_2007.h5'

    # region with alternate naming
    res = request_wind_data('hawaii', 2007)
    assert res == '/nrel/wtk/hawaii/Hawaii_2007.h5'


def test_request_wind_data_invalid_regions():
    """Test invalid region inputs for `request_wind_data`."""
    with pytest.raises(AssertionError) as e:
        request_wind_data('namek', 2007)
    assert str(e.value) == 'region not found: namek' 


def test_request_wind_data_years():
    """Test valid year inputs for `request_wind_data`."""
    # beginning of year range
    res = request_wind_data('canada', 2007)
    assert res == '/nrel/wtk/canada/wtk_canada_2007.h5'

    # end of year range
    res = request_wind_data('canada', 2014)
    assert res == '/nrel/wtk/canada/wtk_canada_2014.h5'

    # between year range
    res = request_wind_data('canada', 2010)
    assert res == '/nrel/wtk/canada/wtk_canada_2010.h5'


def test_request_wind_data_invalid_year():
    """Test invalid year inputs for `request_wind_data`."""
    with pytest.raises(AssertionError) as e:
        request_wind_data('canada', 2015)

    msg = 'year %s not available for region: %s' % (2015, 'canada')
    assert str(e.value) == msg


def test_request_wind_data_resolutions():
    """Test valid resolution inputs for `request_wind_data`."""
    # no input defaults to "hourly"
    res = request_wind_data('mexico', 2010)
    assert res == '/nrel/wtk/mexico/wtk_mexico_2010.h5'

    # "hourly" can be explicitly specified
    res = request_wind_data('mexico', 2010, 'hourly')
    assert res == '/nrel/wtk/mexico/wtk_mexico_2010.h5'

    # "5min"
    res = request_wind_data('mexico', 2010, '5min')
    assert res == '/nrel/wtk/mexico-5min/wtk_mexico_2010.h5'


def test_request_wind_data_invalid_resolution():
    """Test valid resolution inputs for `request_wind_data`."""
    with pytest.raises(AssertionError) as e:
        request_wind_data('canada', 2010, "1min")

    msg = 'resolution "%s" not available for region: %s' % (
        '1min', 'canada')
    assert str(e.value) == msg
