from rest_framework import serializers
import re

def password_strength_validator(password):
    validator_reg=re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]',password)
    if validator_reg:
        return password
    else:
        raise serializers.ValidationError(
            "the password needs to have at least one uppercase letter, one lowercase letter and one number"
        )




