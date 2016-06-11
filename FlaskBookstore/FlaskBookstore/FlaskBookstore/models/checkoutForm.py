from wtforms import Form, TextField, validators


class CheckoutForm(Form):
    name = TextField('Name:', [validators.Regexp(r'\w')])
    address_line1 = TextField('Line 1:', [validators.Required()])
    address_line2 = TextField('Line 2:')
    city = TextField('City:', [validators.Required()])
    state = TextField('State:', [validators.Required()])
    zip = TextField('Zip:', [validators.Required()])
    country = TextField('Country:', [validators.Required()])