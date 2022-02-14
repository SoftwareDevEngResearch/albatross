import json
from rex import WindX
import pandas as pd

from .utils import _load_wtk


def _check_lat_lon(lat_lon):
    """Validates lat/lon inputs."""
    assert isinstance(lat_lon, (list, tuple)), 'lat_lon must be a tuple or list'
    err_msg = 'lat/lon points must be floats'
    assert all([isinstance(x, float) for x in lat_lon]), err_msg
    assert len(lat_lon) == 2, 'lat_lon must have a length of 2'


def identify_regions(lat_lon, coordinates=False):
    """
    Returns the region associated with the given lat/lon point.

    Args:
        lat_lon (:obj:`list` of :obj:`float`): latitude/longitude point to
          access
        coordinates (bool): optionally include a list of all registered
          coordinates for the region (requires HSDS API calls)

    Returns:
        list: list of region names (`coordinates=False`)
        list: list of region dicts with coordinate info (`coordinates=True`)
    """
    _check_lat_lon(lat_lon)

    wtk = _load_wtk()
    lat, lon = lat_lon

    regions = []

    for region in wtk:
        lat_range, lon_range = wtk[region]['lat_lon_range']

        if lat >= lat_range[0] and lat <= lat_range[1]:
            if lon >= lon_range[0] and lon <= lon_range[1]:
                if coordinates:
                    # grab coordinates from most recent year
                    wtk_file = build_wtk_filepath(region, wtk[region]['year_range'][1])

                    with WindX(wtk_file, hsds=True) as f:
                        coordinates = f.coordinates

                        regions.append({region: coordinates})
                else:
                    regions.append(region)

    if len(regions) == 0:
        raise ValueError('No region found for specified lat/lon point.')

    return regions


def build_wtk_filepath(region, year, resolution=None):
    """
    A utility for building WIND Toolkit filepaths.

    Args:
        region (str): region in which the lat/lon point is located (see
          `get_regions`)
        year (int): year to be accessed (see `get_regions`)
        resolution (:obj:`str`, optional): data resolution (see `get_regions`)

    Returns:
        str: The filepath for the requested resource.
    """
    wtk = _load_wtk()
    base_url = '/nrel/wtk/'

    assert region in wtk, 'region not found: %s' % region

    year_range = wtk[region]['year_range']
    year_range = range(year_range[0], year_range[1]+1)
    assert isinstance(year, int), '"year" must be an integer'
    msg = 'year %s not available for region: %s' % (year, region)
    assert year in year_range, msg

    if resolution:
        msg = 'resolution "%s" not available for region: %s' % (
            resolution, region)
        assert resolution in wtk[region]['resolutions'], msg

    base = wtk[region].get('base')

    if resolution == '5min':
        url_region = '%s-%s/' % (region, resolution)
    else:
        url_region = region + '/'

    if base:
        file = '%s_%s.h5' % (base, year)
    else:
        file = 'wtk_%s_%s.h5' % (region, year)

    return base_url + url_region + file


def read_wtk_point_data(wtk_file, lat_lon, params, tree=None, unscale=True,
                        str_decode=True, group=None):
    """
    Reads WIND Toolkit data directly from a file.

    Args:
        wtk_file (:obj:`str`): file path
        lat_lon (:obj:`list` of :obj:`float`): latitude/longitude point to
          access
        params (:obj:`list` of :obj:`str`): A list of parameters to include in
          the dataset
        resolution (:obj:`str`, optional): data resolution (see `get_regions`)
        tree (:obj:`str`, optional): cKDTree or path to .pkl file containing
          pre-computed tree of lat, lon coordinates, by default None
        unscale (:obj:`bool`, optional): Boolean flag to automatically unscale
          variables on extraction, by default True
        str_decode (:obj:`bool`, optional): Boolean flag to decode the
          bytestring meta data into normal strings. Setting this to False will
          speed up the meta data read. by default True
        group (:obj:`str`, optional): Group within .h5 resource file to open,
          by default None

    Returns:
        tuple: A tuple `(data, metadata)` consisting of a `DataFrame` and associated
        metadata.
    """
    _check_lat_lon(lat_lon)

    assert isinstance(params, (list, tuple)), '"params" must be a tuple or list'
    assert len(params) != 0, '"params" must not be empty'
    err_msg = '"params" elements must be strings'
    assert all([isinstance(x, str) for x in params]), err_msg

    kwargs = {
        'tree': tree, 'unscale': unscale, 'str_decode': str_decode,
        'group': group, 'hsds': False
    }

    results = []

    with WindX(wtk_file, **kwargs) as f:
        for param in params:
            meta = f.meta
            res = f.get_lat_lon_df(param, lat_lon)
            col = res.columns[0]
            res.rename(columns={col: param}, inplace=True)
            results.append(res)

    data = pd.concat(results, axis=1)

    return (data, meta)


def request_wtk_point_data(lat_lon, year, params, region=None, resolution=None,
                           tree=None, unscale=True, str_decode=True,
                           group=None):
    """
    Requests WIND Toolkit data from NREL HSDS for a given lat/lon point. If a
    `region` is not specified, it will attempt to infer one using `identify_regions`.
    However, if multiple regions are identified for the `lat_lon` provided, it will
    raise an error, prompting the user to explicitly provide one.

    Args:
        lat_lon (:obj:`list` of :obj:`float`): latitude/longitude point to
          access
        year (int): year to be accessed (see `get_regions`)
        params (:obj:`list` of :obj:`str`): A list of parameters to include in
          the dataset
        region (str, optional): region in which the lat/lon point is located (see
          `get_regions`)
        resolution (:obj:`str`, optional): data resolution (see `get_regions`)
        tree (:obj:`str`, optional): cKDTree or path to .pkl file containing
          pre-computed tree of lat, lon coordinates, by default None
        unscale (:obj:`bool`, optional): Boolean flag to automatically unscale
          variables on extraction, by default True
        str_decode (:obj:`bool`, optional): Boolean flag to decode the
          bytestring meta data into normal strings. Setting this to False will
          speed up the meta data read. by default True
        group (:obj:`str`, optional): Group within .h5 resource file to open,
          by default None

    Returns:
        tuple: A tuple `(data, metadata)` consisting of a `DataFrame` and associated
        metadata.
    """
    _check_lat_lon(lat_lon)

    assert isinstance(params, (list, tuple)), '"params" must be a tuple or list'
    assert len(params) != 0, '"params" must not be empty'
    err_msg = '"params" elements must be strings'
    assert all([isinstance(x, str) for x in params]), err_msg

    if not region:
        regions = identify_regions(lat_lon)

        err_msg = (
            'Multiple regions identified for the given lat/lon point: %s.\n'
            'Please specify one using the `region` arg.'
        ) % regions

        if len(regions) > 1:
            print(err_msg)

        assert len(regions) == 1, err_msg

        region = regions[0]

    wtk_file = build_wtk_filepath(region, year, resolution)

    kwargs = {
        'tree': tree, 'unscale': unscale, 'str_decode': str_decode,
        'group': group, 'hsds': True
    }

    results = []

    with WindX(wtk_file, **kwargs) as f:
        for param in params:
            meta = f.meta
            res = f.get_lat_lon_df(param, lat_lon)
            col = res.columns[0]
            res.rename(columns={col: param}, inplace=True)
            results.append(res)

    data = pd.concat(results, axis=1)

    return (data, meta)


def get_regions(pprint=False):
    """
    Returns the full set of regions with their configuration options.

    Note that the `year_range` represents an inclusive (beginning, end), where
    any specified value within that range is a valid year for that region.

    Args:
        pprint (bool): Pretty print results.

    Returns:
        dict: Regions and configuration options.
    """
    wtk = _load_wtk()
    if pprint:
        print(json.dumps(wtk, indent=4))

    return wtk
