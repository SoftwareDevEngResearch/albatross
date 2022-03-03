import os
import pytest
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pandas import DataFrame, read_hdf

from albatross import TESTDATADIR
from albatross.classes import WindTurbine
from albatross.requests import read_wtk_point_data
from albatross.analysis import (
    boxplot, get_diurnal_stats, plot_diurnal_stats, plot_windrose, pdf, turbulence_std)


@pytest.fixture
def data():
    path = os.path.join(TESTDATADIR, 'ri_100_wtk_2012.h5')
    lat_lon = (41.96364, -71.79364)

    res, meta = read_wtk_point_data(path, lat_lon, ['windspeed_100m'])

    return res


@pytest.fixture
def data_5min():
    path = os.path.join(TESTDATADIR, 'pacwave_5min.h5')
    res = read_hdf(path)

    return res


@pytest.fixture
def turbine():
    return WindTurbine('II', 'B')


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


# test `pdf` #


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


# test get_diurnal_stats


def test_get_diurnal_stats_invalid_data():
    """Test invalid `data` inputs for `get_diurnal_stats`."""
    with pytest.raises(AssertionError) as e:
        get_diurnal_stats({})

    msg = '"data" must be a DataFrame'
    assert str(e.value) == msg


def test_get_diurnal_stats_invalid_speed(data):
    """Test invalid `speed` inputs for `get_diurnal_stats`."""
    with pytest.raises(AssertionError) as e:
        get_diurnal_stats(data, speed=1)

    msg = '"speed" must be a string'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        get_diurnal_stats(data, speed='bad')

    msg = 'column not found: bad'
    assert str(e.value) == msg


def test_get_diurnal_stats(data):
    "Test `get_diurnal_stats`."
    df = get_diurnal_stats(data)

    assert isinstance(df, DataFrame)

    cols = ['Mean', 'Mean+Std', 'Mean-Std', '10th Percentile', 'Median', '90th Percentile']

    for i, col in enumerate(df.columns):
        assert col == cols[i]
        assert len(df[col]) == 24


# Test `plot_diurnal_stats`


def test_plot_diurnal_stats_invalid_data():
    """Test invalid `data` inputs for `plot_diurnal_stats`."""
    with pytest.raises(AssertionError) as e:
        plot_diurnal_stats({})

    msg = '"data" must be a DataFrame'
    assert str(e.value) == msg


def test_plot_diurnal_stats_invalid_speed(data):
    """Test invalid `speed` inputs for `plot_diurnal_stats`."""
    with pytest.raises(AssertionError) as e:
        plot_diurnal_stats(data, speed=1)

    msg = '"speed" must be a string'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        plot_diurnal_stats(data, speed='bad')

    msg = 'column not found: bad'
    assert str(e.value) == msg


def test_plot_diurnal_stats(data):
    """Test `plot_diurnal_stats`."""
    res = plot_diurnal_stats(data)

    assert len(res) == 3

    (fig, ax, df) = res

    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)
    assert isinstance(df, DataFrame)

    # should be 6 lines plotted
    assert len(ax.get_lines()) == 6


# Test `turbulence_std` #


def test_turbulence_std_invalid_data(turbine):
    """Test invalid `data` inputs for `turbulence_std`."""

    with pytest.raises(AssertionError) as e:
        turbulence_std('bad', turbine)

    msg = '"data" must be a float or DataFrame'
    assert str(e.value) == msg


def test_turbulence_std_invalid_turbine(data):
    """Test invalid `turbine` inputs for `turbulence_std`."""

    with pytest.raises(AssertionError) as e:
        turbulence_std(data, 'bad')

    msg = '"turbine" must be a WindTurbine'
    assert str(e.value) == msg


def test_turbulence_std_invalid_speed(data, turbine):
    """Test invalid `speed` inputs for `plot_diurnal_stats`."""
    with pytest.raises(AssertionError) as e:
        turbulence_std(data, turbine, speed=1)

    msg = '"speed" must be a string'
    assert str(e.value) == msg

    with pytest.raises(AssertionError) as e:
        turbulence_std(data, turbine, speed='bad')

    msg = 'column not found: bad'
    assert str(e.value) == msg


def test_turbulence_std(data_5min, turbine):
    """Test `turbulence_std`."""
    # test single data point
    assert turbulence_std(3.9, turbine) == 1.1935

    # test dataset
    res = turbulence_std(data_5min, turbine)

    assert len(res) == 52560
    assert res.columns == ['turbulence_std']

    # check that first turbulence std data point is correct
    d1, d2 = data_5min['windspeed_10m'][:2]
    avg = (d1 + d2)/2
    t1 = res['turbulence_std'][0]

    assert turbulence_std(avg, turbine) == pytest.approx(t1)
