import pint
from django.core.exceptions import ValidationError
from pint import UndefinedUnitError

valid_unit_measurements = ['pound', 'kilogram', 'gram', 'lbs', 'kilo', 'oz', 'kg']


def validate_unit_measurement(value: str):
    ureg = pint.UnitRegistry()
    try:
        single_unit = ureg[value.lower()]
    except UndefinedUnitError as unit_error:
        raise ValidationError(f"'{value}' is not a valid unit of measure")
    except:
        raise ValidationError(f"'{value}' is invalid. Unknown error.")
