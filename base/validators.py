import phonenumbers
from rest_framework.exceptions import ValidationError


def validate_international_phone_number(phone_number, api_field=None):
    allowed_countries = ['IN', 'US']
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_possible_number(parsed_number):
            raise ValidationError({api_field: "Phone Number is not valid"})
        region_code = phonenumbers.region_code_for_number(parsed_number)
        if region_code not in allowed_countries:
            raise ValidationError({api_field: "Phone Number is not valid for the specified country"})
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError({api_field: "Phone Number is not valid"})
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError({api_field: "Phone Number is not valid"})
