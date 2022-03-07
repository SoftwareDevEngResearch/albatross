import pytest

from albatross import WindTurbine, RequestParams


def test_WindTurbine_invalid_speed():
    """Test invalid `wind_speed_class` inputs for `WindTurbine`."""
    with pytest.raises(AssertionError) as e:
        WindTurbine('bad', 'C')

    msg = 'Wind speed classification "bad" not found.'
    assert str(e.value) == msg


def test_WindTurbine_invalid_turb():
    """Test invalid `turbulence_class` inputs for `WindTurbine`."""
    with pytest.raises(AssertionError) as e:
        WindTurbine('I', 'bad')

    msg = 'Turbulence classification "bad" not found.'
    assert str(e.value) == msg


def test_WindTurbine():
    """Test `WindTurbine` initialization."""
    turbine = WindTurbine('I', 'A+')

    assert turbine.v_ave == 10
    assert turbine.v_ref == 50
    assert turbine.v_ref_t == 57
    assert turbine.i_ref == 0.18


# Test RequestParams #

def test_RequestParams_init():
    """Test initialization and class methods for `RequestParams`."""
    fields = RequestParams.get_fields()
    assert len(fields) == 10

    rp = RequestParams()

    assert rp.params == []


def test_RequestParams_register_invalid_field():
    """Test invalid `field` inputs for `register`."""
    rp = RequestParams()

    # bad field
    with pytest.raises(AssertionError) as e:
        rp.register('bad')

    msg = 'Field "bad" not found.'
    assert str(e.value) == msg

    # missing height
    with pytest.raises(AssertionError) as e:
        rp.register('wind_speed')

    msg = '"height" is required for this field.'
    assert str(e.value) == msg

    # invalid height
    with pytest.raises(AssertionError) as e:
        rp.register('wind_speed', height='12')

    msg = '"height" must be an integer.'
    assert str(e.value) == msg

    # height out of range
    with pytest.raises(AssertionError) as e:
        rp.register('wind_speed', height=0)

    msg = '"height" must be in range(10, 201).'
    assert str(e.value) == msg

    assert rp.params == []


def test_RequestParams_register():
    """Test `register`."""
    rp = RequestParams()

    rp.register('wind_speed', height=10)

    assert len(rp.params) == 1
    assert rp.params[0] == 'windspeed_10m'

    rp.register('inverse_monin_obukhov_length')

    assert len(rp.params) == 2
    assert rp.params[1] == 'inversemoninobukhovlength_2m'
