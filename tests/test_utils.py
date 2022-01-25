from albatross import utils

def test_load_wtk():
    wtk = utils._load_wtk()
    assert 'wtk' in wtk
    assert 'conus' in wtk['wtk']
    assert 'year_range' in wtk['wtk']['conus']
    assert 'resolutions' in wtk['wtk']['conus']
