import pytest

from albatross import WindTurbine


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
