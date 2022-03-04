"""
This module defines classes for use in analysis.
"""

WIND_SPEED_CLASSES = {
    'I': {
        'v_ave': 10,
        'v_ref': 50,
        'v_ref_t': 57
    },
    'II': {
        'v_ave': 8.5,
        'v_ref': 42.5,
        'v_ref_t': 57
    },
    'III': {
        'v_ave': 7.5,
        'v_ref': 37.5,
        'v_ref_t': 57
    },
}


TURBULENCE_CLASSES = {
    'A+': {
        'i_ref': 0.18
    },
    'A': {
        'i_ref': 0.16
    },
    'B': {
        'i_ref': 0.14
    },
    'C': {
        'i_ref': 0.12
    },
}


class WindTurbine:
    """
    Represents a wind turbine that follows classification guidelines for IEC-61400, Section 6.2.

    Turbines are classified in terms of both wind speed and turbulence. Wind speed categories are
    I, II, III; and turbulence categories are A+, A, B, C. Each category has associated
    reference values that may be used in calculations. Custom implementations (Class S) are
    not yet supported.

    .. image:: ../docs/turbine_classification.png
    """
    def __init__(self, wind_speed_class, turbulence_class):
        """
        Args:
          wind_speed_class (str): A wind speed classification.
          turbulence_class (str): A turbulence classification.
        """
        self._validate_wind_speed_class(wind_speed_class)
        self._validate_turbulence_class(turbulence_class)

        self.wind_speed_class = wind_speed_class
        self.turbulence_class = turbulence_class

        self._set_turbine_data()
        self._set_turbulence_data()

    def _validate_wind_speed_class(self, wind_speed_class):
        msg = 'Wind speed classification "%s" not found.' % wind_speed_class
        assert wind_speed_class in WIND_SPEED_CLASSES, msg

    def _validate_turbulence_class(self, turbulence_class):
        msg = 'Turbulence classification "%s" not found.' % turbulence_class
        assert turbulence_class in TURBULENCE_CLASSES, msg

    def _set_turbine_data(self):
        self.v_ave = WIND_SPEED_CLASSES[self.wind_speed_class]['v_ave']
        self.v_ref = WIND_SPEED_CLASSES[self.wind_speed_class]['v_ref']
        self.v_ref_t = WIND_SPEED_CLASSES[self.wind_speed_class]['v_ref_t']

    def _set_turbulence_data(self):
        self.i_ref = TURBULENCE_CLASSES[self.turbulence_class]['i_ref']
