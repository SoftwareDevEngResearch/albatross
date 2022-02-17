import os

import pytest

from matplotlib.figure import Figure
from matplotlib.axes import Axes

from albatross import TESTDATADIR
from albatross.requests import read_wtk_point_data
from albatross.analysis import boxplot, plot_windrose, pdf


@pytest.fixture
def data():
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    data, meta = read_wtk_point_data(path, lat_lon, ['windspeed_100m'])

    return data


def test_boxplot_invalid_data():
    """Test invalid `data` inputs for `boxplot`."""
    with pytest.raises(AssertionError) as e:
        boxplot({})

    msg = '"data" must be a DataFrame'
    assert str(e.value) == msg


def test_boxplot_invalid_fields(data):
    """Test invalid `fields` inputs for `boxplot`."""
    with pytest.raises(AssertionError) as e:
        boxplot(data, fields='bad')

    msg = '"fields" must be a list or None'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        boxplot(data, fields=[1])

    msg = '"fields" elements must be strings'
    assert str(e.value) == msg


def test_boxplot_invalid_labels(data):
    """Test invalid `labels` inputs for `boxplot`."""
    with pytest.raises(AssertionError) as e:
        boxplot(data, labels='bad')

    msg = '"labels" must be a list or None'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        boxplot(data, labels=[1])

    msg = '"labels" elements must be strings'
    assert str(e.value) == msg


def test_boxplot(data):
    """Test invalid `data` inputs for `boxplot`."""
    boxplot(data)

    # TODO: add image comparison testing https://matplotlib.org/stable/devel/testing.html#writing-an-image-comparison-test # noqa


# Test `plot_windrose` #

def test_windrose_invalid_data():
    """Test invalid `data` inputs for `plot_windrose`."""
    with pytest.raises(AssertionError) as e:
        plot_windrose({})

    msg = '"data" must be a DataFrame'
    assert str(e.value) == msg


def test_windrose_invalid_speed(data):
    """Test invalid `speed` inputs for `plot_windrose`."""
    with pytest.raises(AssertionError) as e:
        plot_windrose(data, speed=1)

    msg = '"speed" must be a string'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        plot_windrose(data, speed='bad')

    msg = 'column not found: bad'
    assert str(e.value) == msg


def test_windrose_invalid_direction(data):
    """Test invalid `direction` inputs for `plot_windrose`."""
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


# test `pdf`


def test_pdf_invalid_kwargs(data):
    """Test invalid `_kwargs` inputs for `pdf`."""

    with pytest.raises(AssertionError) as e:
        pdf(data, hist_kwargs='bad')

    msg = '"hist_kwargs" must be a dict'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        pdf(data, plot_kwargs='bad')

    msg = '"plot_kwargs" must be a dict'
    assert str(e.value) == msg


def test_pdf_invalid_speed(data):
    """Test invalid `speed` inputs for `pdf`."""
    with pytest.raises(AssertionError) as e:
        pdf(data, speed=1)

    msg = '"speed" must be a string'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        pdf(data, speed='bad')

    msg = 'column not found: bad'
    assert str(e.value) == msg


def test_pdf(data):
    """Test `pdf`."""
    res = pdf(data)
    assert len(res) == 3

    fig, ax, params = res

    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)
    assert len(params) == 4
    assert all([isinstance(x, (float, int)) for x in params])

    # TODO: add image comparison testing https://matplotlib.org/stable/devel/testing.html#writing-an-image-comparison-test # noqa
