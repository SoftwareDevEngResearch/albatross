"""
Provides analysis tools for wind data.
"""

import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame, Grouper
from windrose import WindroseAxes
from scipy import stats
import numpy as np

from .classes import WindTurbine


def boxplot(data, fields=None, labels=None, **box_kwargs):
    """
    Draws boxplots of wind speeds.

    Args:
      data (DataFrame): wind data
      fields (:obj:`list` of :obj:`str`, optional): a list of columns to include from the
        given `data`. If none are provided, these will be inferred using any columns in
        `data` with the prefix `'windspeed_'`.
      labels (:obj:`list` of :obj:`str`, optional): a list of labels to use. If none are
        provided, they will use the same names as `fields`. If no `fields` or `labels`
        are provided, they will both be inferred using the same strategy as `fields`, but
        taking the suffix after `'windspeed_'`. e.g. `'windspeed_90m'` -> `'90m'`
      box_kwargs (dict, optional): additional parameters for `matplotlib.pyplot.boxplot`

    Returns:
      tuple: A tuple (fig, ax) consisting of a `matplotlib.figure.Figure` and
      `matplotlib.axes.Axes`.
    """
    assert isinstance(data, DataFrame), '"data" must be a DataFrame'

    if fields:
        assert isinstance(fields, list), '"fields" must be a list or None'
        msg = '"fields" elements must be strings'
        assert all([isinstance(f, str) for f in fields]), msg

    if labels:
        assert isinstance(labels, list), '"labels" must be a list or None'
        msg = '"labels" elements must be strings'
        assert all([isinstance(label, str) for label in labels]), msg
    else:
        labels = fields

    if not fields and not labels:
        fields = list(filter(lambda x: 'windspeed' in x, data.columns[:]))
        labels = [field.split('_')[1] for field in fields]

    x = [list(data[field]) for field in fields]
    fig, ax = plt.subplots()
    ax.boxplot(
        x,
        labels=labels,
        flierprops=dict(marker='_', markeredgecolor='red'),
        boxprops=dict(color='blue'),
        medianprops=dict(color='red'), **box_kwargs)
    ax.set_ylabel('Wind Speed (m/s)', fontsize='large')
    ax.set_xlabel('Elevation (m)', fontsize='large')

    return fig, ax


def plot_windrose(data, speed=None, direction=None, **wr_kwargs):
    """
    Generates a windrose plot from the given data.

    Args:
      data (DataFrame): Wind data
      speed (str, optional): Wind speed column name. If not provided, it will be inferred
        from `data`. It will take the first column containing the string 'windspeed'.
      direction (str, optional): Wind direction column name. If not provided, it will be
        inferred from `data`. It will take the first column containing the string `winddirection`.
      wr_kwargs (dict, optional): Additional windrose parameters. See
        https://windrose.readthedocs.io for more info.

    Returns:
      WindroseAxes: A `WindroseAxes` instance.
    """
    assert isinstance(data, DataFrame), '"data" must be a DataFrame'

    if speed:
        assert isinstance(speed, str), '"speed" must be a string'
        assert speed in data, "column not found: %s" % speed
        ws = list(data[speed])
    if direction:
        assert isinstance(direction, str), '"direction" must be a string'
        assert direction in data, 'column not found: %s' % direction
        wd = list(data[direction])

    if not speed:
        fields = list(filter(lambda x: 'windspeed' in x, data.columns[:]))
        assert len(fields) > 0, 'unable to infer wind speed data column'
        ws_field = fields[0]
        ws = list(data[ws_field])

    if not direction:
        fields = list(filter(lambda x: 'winddirection' in x, data.columns[:]))
        assert len(fields) > 0, 'unable to infer wind direction data column'
        wd_field = fields[0]
        wd = list(data[wd_field])

    # NOTE: this is a workaround for a current bug in the `windrose` package
    ax = WindroseAxes.from_ax(theta_labels=["E", "N-E", "N", "N-W", "W", "S-W", "S", "S-E"])
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white', **wr_kwargs)
    ax.set_legend()

    return ax


def pdf(data, speed=None, hist_kwargs=None, plot_kwargs=None):
    """
    Generates a windrose plot from the given data.

    Args:
      data (DataFrame): Wind data
      speed (str, optional): Wind speed column name. If not provided, it will be inferred
        from `data`. It will take the first column containing the string 'windspeed'.
      hist_kwargs (dict, optional): Additional histogram parameters.
      plot_kwargs (dict, optional): Additional plot parameters.

    Returns:
      tuple: (fig, ax, params) consisting of a `matplotlib.figure.Figure`,
      `matplotlib.axes.Axes`, and 4-element tuple of floats/ints representing
      shape (2), location, and scale.
    """
    assert isinstance(data, DataFrame), '"data" must be a DataFrame'

    plot_kwargs = plot_kwargs or {}
    hist_kwargs = hist_kwargs or {}

    assert isinstance(plot_kwargs, dict), '"plot_kwargs" must be a dict'
    assert isinstance(hist_kwargs, dict), '"hist_kwargs" must be a dict'

    if speed:
        assert isinstance(speed, str), '"speed" must be a string'
        assert speed in data, "column not found: %s" % speed
        ws = list(data[speed])
    else:
        fields = list(filter(lambda x: 'windspeed' in x, data.columns[:]))
        assert len(fields) > 0, 'unable to infer wind speed data column'
        ws_field = fields[0]
        ws = list(data[ws_field])

    # Fit Weibull function
    params = stats.exponweib.fit(ws, floc=0, f0=1)

    # Plotting

    fig, ax = plt.subplots()

    # Histogram
    bins = round(max(ws))+5
    values, bins, hist = ax.hist(ws, bins=bins, density=True, lw=1, ec='black', **hist_kwargs)
    center = (bins[:-1] + bins[1:]) / 2.

    # Using all params and the `pdf` function
    ax.plot(
        center,
        stats.exponweib.pdf(center, *params),
        lw=2, label='Weibull', color='r', **plot_kwargs)

    ax.set_xlabel('Wind Speed (m/s)', fontsize='large')
    ax.set_ylabel('Probability Density', fontsize='large')
    ax.legend()

    return fig, ax, params


def get_diurnal_stats(data, speed=None):
    """
    Returns basic relevant diurnal wind speed statistics for the given data.

    Args:
      data (DataFrame): Wind data
      speed (str, optional): Wind speed column name. If not provided, it will be inferred
        from `data`. It will take the first column containing the string 'windspeed'.

    Returns:
      DataFrame: A DataFrame consisting of an hourly time index, and columns representing
      various diurnal wind speed statistics for the given wind speed.
    """
    assert isinstance(data, DataFrame), '"data" must be a DataFrame'
    if speed:
        assert isinstance(speed, str), '"speed" must be a string'
        assert speed in data, "column not found: %s" % speed
        ws = data[speed]
    else:
        fields = list(filter(lambda x: 'windspeed' in x, data.columns[:]))
        assert len(fields) > 0, 'unable to infer wind speed data column'
        ws_field = fields[0]
        ws = data[ws_field]

    mean = ws.groupby(data.index.hour).mean()
    plus_std = mean + ws.groupby(data.index.hour).std()
    minus_std = mean - ws.groupby(data.index.hour).std()
    p_10 = ws.groupby(data.index.hour).quantile(q=.1)
    median = ws.groupby(data.index.hour).median()
    p_90 = ws.groupby(data.index.hour).quantile(q=.9)

    df = pandas.concat([mean, plus_std, minus_std, p_10, median, p_90], axis=1)

    df.columns = ['Mean', 'Mean+Std', 'Mean-Std', '10th Percentile', 'Median', '90th Percentile']

    return df


def plot_diurnal_stats(data, speed=None):
    """
    Plots basic relevant diurnal wind speed statistics for the given data.

    Args:
      data (DataFrame): Wind data
      speed (str, optional): Wind speed column name. If not provided, it will be inferred
        from `data`. It will take the first column containing the string 'windspeed'.

    Returns:
      tuple: A tuple (fig, ax, df) consisting of a `matplotlib.figure.Figure`,
      `matplotlib.axes.Axes`, and a `pandas.DataFrame` (same data as `get_diurnal_stats`).
    """

    # data/field validation performed in this function
    stats_df = get_diurnal_stats(data, speed)

    markers = ('+', '*', '.', '2', 'x', '')

    fig, ax = plt.subplots()

    for i, label in enumerate(stats_df):
        ax.plot(stats_df[label], label=label, marker=markers[i])

    ax.set_xlabel('Hour')
    ax.set_ylabel('Wind Speed (m/s)')
    ax.set_xticks(np.arange(0, 23, 2))
    ax.legend()

    return fig, ax, stats_df


def turbulence_std(data, turbine, speed=None, b=5.6):
    """
    Calculates the turbulence standard deviation.

    Args:
      data (Union[float, DataFrame]): Wind speed velocity (m/s) at hub height.
      turbine (WindTurbine): A `WindTurbine` instance.
      b (float, optional): Additional adjustment parameter (m/s)

    Returns:
      float: Turbulence standard deviation.
    """
    assert isinstance(data, (float, DataFrame)), '"data" must be a float or DataFrame'
    assert isinstance(turbine, WindTurbine), '"turbine" must be a WindTurbine'

    if isinstance(data, float):
        return turbine.i_ref*(0.75*data + b)

    if speed:
        assert isinstance(speed, str), '"speed" must be a string'
        assert speed in data, "column not found: %s" % speed
        ws = data[speed]
    else:
        fields = list(filter(lambda x: 'windspeed' in x, data.columns[:]))
        assert len(fields) > 0, 'unable to infer wind speed data column'
        ws_field = fields[0]
        ws = data[ws_field]

    # Group wind speeds by 10min averages, should work for any resolution
    ws_avg = ws.groupby(Grouper(freq='10min')).mean()
    df = DataFrame(ws_avg)
    df.columns = ['turbulence_std']

    # Apply std calc for every row
    df = df.apply(lambda d: turbine.i_ref*(0.75*d + b))

    return df
