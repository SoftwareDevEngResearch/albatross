import os

import pytest

from albatross import TESTDATADIR
from albatross.requests import read_wtk_point_data
from albatross.analysis import boxplot, plot_windrose


def test_boxplot_invalid_data():
    """Test invalid `data` inputs for `boxplot`."""
    with pytest.raises(AssertionError) as e:
        boxplot({})

    msg = '"data" must be a DataFrame'
    assert str(e.value) == msg


def test_boxplot_invalid_fields():
    """Test invalid `fields` inputs for `boxplot`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    data, _ = read_wtk_point_data(path, lat_lon, ['windspeed_100m'])

    with pytest.raises(AssertionError) as e:
        boxplot(data, fields='bad')

    msg = '"fields" must be a list or None'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        boxplot(data, fields=[1])

    msg = '"fields" elements must be strings'
    assert str(e.value) == msg


def test_boxplot_invalid_labels():
    """Test invalid `labels` inputs for `boxplot`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    data, _ = read_wtk_point_data(path, lat_lon, ['windspeed_100m'])

    with pytest.raises(AssertionError) as e:
        boxplot(data, labels='bad')

    msg = '"labels" must be a list or None'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        boxplot(data, labels=[1])

    msg = '"labels" elements must be strings'
    assert str(e.value) == msg


def test_boxplot():
    """Test invalid `data` inputs for `boxplot`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    data, _ = read_wtk_point_data(path, lat_lon, ['windspeed_100m'])

    boxplot(data)

    # TODO: add image comparison testing https://matplotlib.org/stable/devel/testing.html#writing-an-image-comparison-test # noqa


# Test `plot_windrose` #

def test_windrose_invalid_data():
    """Test invalid `data` inputs for `plot_windrose`."""
    with pytest.raises(AssertionError) as e:
        plot_windrose({})

    msg = '"data" must be a DataFrame'
    assert str(e.value) == msg


def test_windrose_invalid_speed():
    """Test invalid `speed` inputs for `plot_windrose`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    data, _ = read_wtk_point_data(path, lat_lon, ['windspeed_100m'])

    with pytest.raises(AssertionError) as e:
        plot_windrose(data, speed=1)

    msg = '"speed" must be a string'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        plot_windrose(data, speed='bad')

    msg = 'column not found: bad'
    assert str(e.value) == msg


def test_windrose_invalid_direction():
    """Test invalid `direction` inputs for `plot_windrose`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    data, _ = read_wtk_point_data(path, lat_lon, ['winddirection_100m'])

    with pytest.raises(AssertionError) as e:
        plot_windrose(data, direction=1)

    msg = '"direction" must be a string'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        plot_windrose(data, direction='bad')

    msg = 'column not found: bad'
    assert str(e.value) == msg


def test_windrose_failed_inference():
    """Test failed inference for speed and direction in `plot_windrose`."""

    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    data, _ = read_wtk_point_data(path, lat_lon, ['winddirection_100m'])

    with pytest.raises(AssertionError) as e:
        plot_windrose(data)

    msg = 'unable to infer wind speed data column'
    assert str(e.value) == msg

    data, _ = read_wtk_point_data(path, lat_lon, ['windspeed_100m'])

    with pytest.raises(AssertionError) as e:
        plot_windrose(data)

    msg = 'unable to infer wind direction data column'
    assert str(e.value) == msg


def test_windrose():
    """Test `plot_windrose`."""
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    # happy path
    data, _ = read_wtk_point_data(path, lat_lon, ['windspeed_100m', 'winddirection_100m'])

    plot_windrose(data)

    # explicit columns
    data, _ = read_wtk_point_data(path, lat_lon, ['windspeed_100m', 'winddirection_100m'])

    data.rename(columns={'windspeed_100m': 'ws', 'winddirection_100m': 'wd'}, inplace=True)

    plot_windrose(data, speed='ws', direction='wd')
