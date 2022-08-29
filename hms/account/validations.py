import datetime
import re

from rest_framework import serializers


def is_contact_valid(s):
    # 1) Begins with 0 or 91
    # 2) Then contains 7 or 8 or 9.
    # 3) Then contains 9 digits
    check_pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    if not check_pattern.match(s):
        raise serializers.ValidationError(
            "Mobile should begin with 0 or 91 then contain 7 or 8 or 9  then contains 9 digits.")
    else:
        return True


def check_password_match(password, password2):
    # Check if passwords match
    if password != password2:
        raise serializers.ValidationError("Password and confirm Password does not match.")
    else:
        return True


def check_birthdate(birthdate):
    #  Check if birthdate entered is not in the future
    print(f'Birthdate {birthdate}')
    if birthdate > datetime.date.today():
        raise serializers.ValidationError("Please enter valid birth date.")
    else:
        return True
