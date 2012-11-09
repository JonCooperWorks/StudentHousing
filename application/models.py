from google.appengine.ext import db

class Landlord(db.Model):
    name = db.StringProperty()
    phone_number = db.StringProperty()
    email_address = db.EmailProperty()
    created_on = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()
    
    @staticmethod
    def get_by_user(user):
        query = db.GqlQuery("SELECT * FROM Landlord WHERE user = :1", user)
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
    landlord = db.ReferenceProperty(Landlord)
    renter = db.ReferenceProperty(Renter)
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
    query = db.GqlQuery("SELECT * FROM Landlord WHERE user= :1", user)
    landlord = query.get()
    if landlord is not None:
        return landlord.name
    else:
        return "Anonymous"

def is_account(user):
    account = db.GqlQuery("SELECT name FROM Landlord WHERE user= :1", user).get()
    return account is not None

class Review(db.Model):
    title = db.StringProperty()
    body = db.StringProperty()
    timestamp = db.DateTimeProperty()
    rating = db.IntegerProperty()
    poster = db.UserProperty()
    listing = db.ReferenceProperty(Listing)

class Renter(db.Model):
    name = db.StringProperty()
    phone_number = db.StringProperty()
    email_address = db.StringProperty()
    created_on = db.DateTimeProperty()
    user = db.UserProperty()