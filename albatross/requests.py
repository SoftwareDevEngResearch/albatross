import json
from .utils import _load_wtk

def _build_url(region, year, resolution=None):
    wtk = _load_wtk()
    base_url = '/nrel/wtk/'

    assert region in wtk, 'region not found: %s' % region

    year_range = wtk[region]['year_range']
    year_range = range(year_range[0], year_range[1]+1)

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


def request_wind_data(region, year, resolution=None):
    url = _build_url(region, year, resolution)

    return url


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
