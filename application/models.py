from google.appengine.ext import db

class Contact(db.Model):
    name = db.StringProperty()
    phone_number = db.StringProperty()
    email_address = db.EmailProperty()
    created_on = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()
    
    @staticmethod
    def get_by_user(user):
        query = db.GqlQuery("SELECT * FROM Contact WHERE user = :1", user)
        return query.get()

class Listing(db.Model):
    title = db.StringProperty()
    address = db.StringProperty()
    city = db.StringProperty()
    parish = db.IntegerProperty()
    description = db.TextProperty()
    occupancy = db.IntegerProperty()
    rent = db.FloatProperty()
    occupied = db.BooleanProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)
    landlord = db.ReferenceProperty(Contact)
    user = db.UserProperty()
    
    @staticmethod
    def get_by_user(user):
        query = db.GqlQuery("SELECT * FROM Listing WHERE user = :1 ORDER BY occupied, timestamp DESC", user)
        return query.run()
    
    @staticmethod
    def delete_by_id(id):
        listing = Listing.get_by_id(id)
        db.delete(listing)
    
def get_username(user):
    query = db.GqlQuery("SELECT * FROM Contact WHERE user= :1", user)
    contact = query.get()
    if contact is not None:
        return contact.name
    else:
        return "Anonymous"

def is_account(user):
    account = db.GqlQuery("SELECT name FROM Contact WHERE user= :1", user).get()
    return account is not None