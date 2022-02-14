import os

import pytest

from albatross import TESTDATADIR
from albatross.requests import read_wtk_point_data
from albatross.analysis import boxplot


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
