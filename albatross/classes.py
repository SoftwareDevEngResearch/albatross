"""
This module defines classes for use in requests/analysis.
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


class RequestParams:
    """
    Streamlines request parameter formation.
    """
    def __init__(self):
        self.params = []

    _OTHER_FIELDS = {
        'time_index': 'time_index',
        'meta': 'meta',
        'coordinates': 'coordinates',
        'inverse_monin_obukhov_length': 'inversemoninobukhovlength_2m',
        'relative_humidity': 'relativehumidity_2m',
        'precipitation_rate': 'precipitationrate_0m'
    }
    _HEIGHT_FIELDS = {
        'wind_speed': {
            'field': 'windspeed',
            'height_range': range(10, 201)
        },
        'wind_direction': {
            'field': 'winddirection',
            'height_range': range(10, 201)
        },
        'pressure': {
            'field': 'pressure',
            'height_range': range(0, 201)
        },
        'temperature': {
            'field': 'temperature',
            'height_range': range(2, 201)
        }
    }

    @classmethod
    def get_fields(cls):
        """
        Returns a list of fields that can be used as parameters.
        
        Returns:
          list: A list of valid parameters:

            - wind_speed (`height` required when registering)

            - wind_direction (`height` required when registering)

            - pressure (`height` required when registering)

            - temperature (`height` required when registering)

            - time_index (timescale information)

            - meta (metadata information)

            - coordinates (a list of all lat/lon coordinates for this dataset)

            - inverse_monin_obukhov_length

            - relative_humidity

            - precipitation_rate
        """
        height = [f for f in cls._HEIGHT_FIELDS]
        other = [f for f in cls._OTHER_FIELDS]

        return height + other

    def register(self, field, height=None):
        """
        Registers a new request field.
        
        Args:
          field (str): A field name. Must be a valid field name (see `RequestParams.get_fields`)
          height (int): A height (m). Must fall into the following ranges (inclusive):

            - wind_speed: 10-200

            - wind_direction: 10-200

            - pressure: 0-200

            - temperature: 2-200

        """
        msg = f'Field "{field}" not found.'
        assert field in self._HEIGHT_FIELDS or field in self._OTHER_FIELDS, msg

        if field in self._HEIGHT_FIELDS:
            assert height is not None, '"height" is required for this field.'
            assert isinstance(height, int), '"height" must be an integer.'
            height_range = self._HEIGHT_FIELDS[field]['height_range']
            msg = f'"height" must be in {height_range}.'
            assert height in height_range, msg

            field_name = self._HEIGHT_FIELDS[field]['field']
            self.params.append(f'{field_name}_{height}m')
        else:
            self.params.append(self._OTHER_FIELDS[field])
