"""
Provides analysis tools for wind data.
"""

import matplotlib.pyplot as plt
from pandas import DataFrame


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

    if not fields and not labels:
        fields = list(filter(lambda x: 'windspeed' in x, data.columns[:]))
        labels = [field.split('_')[1] for field in fields]

    if not labels:
        labels = fields

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
