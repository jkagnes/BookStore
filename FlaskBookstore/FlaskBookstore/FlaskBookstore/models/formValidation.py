import re


class FormValidation(object):

    def __init__(self):
        self.x = ""


    def validate_form_field(self, field, pattern):
        if re.match(pattern, field):
            return True
        else:
            return False


    def validate_name(self, name):
        namePattern = "^[a-zA-Z ,.'-]+$"
        return self.validate_form_field(name, namePattern)


    def validate_address(self, address):
        addressPattern = "[A-Za-z0-9'\.\-\s\,]"
        return self.validate_form_field(address, addressPattern)


    def validate_city(self, city):
        cityPattern = "^[A-Za-z\s\-]+$"
        return self.validate_form_field(city, cityPattern)


    def validate_state(self, state):
        statePattern = "^[A-Za-z]"
        return self.validate_form_field(state, statePattern)


    def validate_zip(self, zip):
        zipPattern = "^\d{5}(?:[-\s]\d{4})?$"
        return self.validate_form_field(zip, zipPattern)


    def validate_country(self, country):
        countryPattern = "^[A-Za-z\s\-]+$"
        return self.validate_form_field(country, countryPattern)
