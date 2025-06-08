from django.core.validators import RegexValidator

phone_and_fax_number_validator = RegexValidator(
    regex=r'\A\+?[\d \-\(\)]+\Z',
    message=(
        'Enter a valid phone number. Allowed characters: optional leading +, digits, spaces, parentheses, and dashes.'
    )
)
