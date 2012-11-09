from flaskext import wtf
from flaskext.wtf import validators
<<<<<<< HEAD

#List of parishes for form
parishes = [
    (1, "Kingston"),
    (2, "St. Andrew"),
    (3, "St. Catherine"),
    (4, "Clarendon"),
    (5, "Manchester"),
    (6, "St. Elizabeth"),
    (7, "Westmoreland"),
    (8, "Hanover"),
    (9, "St. James"),
    (10, "Trelawny"),
    (11, "St. Ann"),
    (12, "St. Mary"),
    (13, "Portland"),
    (14, "St. Thomas")
]

occupancies = [
    (1, 'Single'), 
    (2, 'Double'), 
    (3, 'Triple'), 
    (4, 'Multiple')
]

ratings = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
]
=======
from filters import parishes, occupancies
>>>>>>> d76fc545aab7b1e1556c2efea62c18d4a20978f6

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
    
<<<<<<< HEAD
class LandlordForm(wtf.Form):
=======
class ContactForm(wtf.Form):
>>>>>>> d76fc545aab7b1e1556c2efea62c18d4a20978f6
    name = wtf.TextField('Name', validators=[validators.Required(), is_valid_header])
    subject = wtf.TextField('Subject',validators=[validators.Required(), is_valid_header])
    body = wtf.TextAreaField('Message Body',validators=[validators.Required()], widget=wtf.TextArea())
    
class EditListingForm(ListingForm):
<<<<<<< HEAD
    occupied = wtf.BooleanField('Occupied')

class RenterForm(wtf.Form):
    name = wtf.TextField('Name', validators=[validators.Required()])
    phone_number = wtf.TextField('Phone Number', validators=[validators.Required(), is_phone_number()])
    email_address = wtf.TextField('Email Address', validators=[validators.Required(), validators.Email()])

class ReviewForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required()])
    body = wtf.TextAreaField('Review', validators=[validators.Review()])
    rating = wtf.SelectField('Rating', choices=ratings, coerce=int)
=======
    occupied = wtf.BooleanField('Occupied')
>>>>>>> d76fc545aab7b1e1556c2efea62c18d4a20978f6
