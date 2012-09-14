from flaskext import wtf
from flaskext.wtf import validators
from filters import parishes, occupancies

'''Validators'''
def is_phone_number(form, field):
    digits = filter(lambda x: x.isdigit(),field.data)
    if len(digits) != 10 and len(digits) != 7:
        raise validators.ValidationError(u'Invalid phone number')

def is_valid_header(form, field):
    if '\n' in field.data or '\r' in field.data:
        raise validators.ValidationError(u'Email headers cannot contain newlines')

'''Form models'''
class ListingForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required()])
    address = wtf.TextField('Address', validators=[validators.Required()])
    city = wtf.TextField('City',validators=[validators.Required()])
    parish = wtf.SelectField('Parish', choices=parishes, coerce=int)
    description = wtf.TextAreaField('Description')
    occupancy = wtf.SelectField('Occupancy', choices=occupancies, coerce=int)
    rent =  wtf.DecimalField('Rent')
    
class RegistrationForm(wtf.Form):
    name = wtf.TextField('Name',validators=[validators.Required()])
    phone_number = wtf.TextField('Phone Number', validators=[validators.Required(),is_phone_number])
    email_address = wtf.TextField('Email Address', validators=[validators.Required(),validators.Email()])
    
class ContactForm(wtf.Form):
    name = wtf.TextField('Name', validators=[validators.Required(), is_valid_header])
    subject = wtf.TextField('Subject',validators=[validators.Required(), is_valid_header])
    body = wtf.TextAreaField('Message Body',validators=[validators.Required()], widget=wtf.TextArea())
    
class EditListingForm(ListingForm):
    occupied = wtf.BooleanField('Occupied')