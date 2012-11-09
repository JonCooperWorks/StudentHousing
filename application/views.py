import logging, traceback

from google.appengine.api import mail
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect, request, session

from settings import EMAIL_ADDR

from models import Listing, Landlord
from models import is_account, get_username

from forms import ListingForm, RegistrationForm, LandlordForm, EditListingForm

from decorators import login_required, admin_required, account_required

'''Static page views'''

def home():
    return render_template('home.html')

@login_required    
def landlord():
    form = LandlordForm()
    if form.validate_on_submit():
        if send_email(form, 'j.cooper@outlook.com', 'Jonathan Cooper'):
            flash(u'Email sent!', 'success')
            return redirect(url_for('landlord_me'))
        else:
            flash(u'Sending Failed', 'error')
            return redirect(url_for('landlord_me'))
    return render_template('landlord_me.html', form=form)
    
def about():
    return render_template('about.html')
    
'''Landlord only views'''

@login_required
def authenticate():
    '''Allow for account creation'''
    if is_account(users.get_current_user()):
        session['username'] = get_username(users.get_current_user())
        session['logged_in'] = True
        flash(u'Login successful','success')
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        landlord = Landlord(
            name = form.name.data,
            email_address = form.email_address.data,
            phone_number = form.phone_number.data,
            user = users.get_current_user()
        )
        try:
            landlord.put()
            flash(u'Account %s registered successfully'% form.name.data, 'success')
        except CapabilityDisabledError:
            flash(u'The database is currently in read-only mode. We apologize for the inconvenience. Please try again later', 'info')
            logging.error(traceback.extract_stack())
        finally:
            return redirect(url_for('profile'))
    else:
        return render_template('register.html', form=form)
 
@account_required
def add_listing():
    '''Add a listing to the database'''
    form = ListingForm()
    if form.validate_on_submit():
        try:
            persist_listing(form, Listing())
            flash(u'Listing %s successfully saved to database' % listing.key().id(), 'success')
        except CapabilityDisabledError:
            flash(u'The database is currently in read-only mode. We apologize for the inconvenience. Please try again later', 'info')
            logging.error(traceback.extract_stack())
        except TransactionFailedError:
            logging.error(traceback.extract_stack())
            flash(u'Error saving item to database', 'error')
        finally:
            return redirect(url_for('all_listings'))
    else:
        return render_template('add_listing.html', form=form)

@account_required
def manage_listings():
    '''Manage listings'''
    '''Get all listings in database'''
    listings = Listing.get_by_user(users.get_current_user())
    return render_template('manage_listings.html', listings=listings)

@account_required
def manage_listing(id):
    listing = Listing.get_by_id(id)
    if listing is None:
        flash(u'No listing with that ID in database')
        return redirect(url_for('manage_listings'))
    form = EditListingForm(obj=listing)
    if form.validate_on_submit():
        try:
            persist_listing(form, listing)
            flash(u'Listing %s successfully updated' % listing.key().id(), 'success')
        except CapabilityDisabledError:
            flash(u'The database is currently in read-only mode. We apologize for the inconvenience. Please try again later', 'info')
        except TransactionFailedError:
            logging.error('There was an error saving the item to database')
            flash(u'Error saving item to database, please try again later', 'error')
        finally:
            return redirect(url_for('manage_listings'))
    return render_template('manage_listing.html', form=form, listing=listing)

@account_required    
def delete_listing(id):
    '''Delete a listing'''
    listing = Listing.get_by_id(id)
    if(request.method == 'POST') and listing.user == users.get_current_user():
        listing.delete()
        flash(u'Listing deleted successfully', 'success')
        return redirect(url_for('manage_listings'))
    else:
        flash(u'You do not have permissions to perform that operation', 'error')
        return redirect(url_for('profile'))
        
@account_required
def profile():
    '''Landlord management dashboard.'''
    user = users.get_current_user()
    landlord = Landlord.get_by_user(user)
    #Generate statistics for the landlord's listings
    listings = Listing.gql('WHERE user = :1', user).count()
    available = Listing.gql('WHERE user = :1 AND occupied = False', user).count()
    occupied = listings - available
    stats = { 'listings' : listings, 'available' : available, 'occupied' : occupied }
    return render_template('dashboard.html', landlord=landlord, stats=stats)
    
@account_required
def update_landlord():
    '''Allow user to update their landlord information'''
    landlord = Landlord.get_by_user(users.get_current_user())
    form = RegistrationForm(obj=landlord)
    if form.validate_on_submit():
        landlord.name = form.name.data
        landlord.email_address = form.email_address.data
        landlord.phone_number = form.phone_number.data
        try:
            landlord.put()
            flash(u'Information updated successfully', 'success')
        except TransactionFailedError:
            logging.error(traceback.extract_stack())
            flash(u'Error saving landlord details. Try again later', 'error')
        finally:
            return redirect(url_for('profile'))
    return render_template('edit_landlord.html',landlord=landlord,form=form)

@account_required
def logout():
    '''Logs a user out'''
    session.pop('logged_in', None)
    session.pop('username', None)
    flash(u'You were logged out!', 'success')
    return redirect(users.create_logout_url(url_for('home')))

'''No authentication required'''

def all_listings():
    '''Get all active listings in database'''
    listings = Listing.all().filter('occupied =', False).order('-timestamp')
    return render_template('listings.html', listings=listings)

def listings_by_parish(id):
    '''Get all active listings by parish'''
    listings = Listing.gql("WHERE parish = :1 AND occupied = False ORDER BY timestamp DESC", id)
    return render_template('listings.html', listings=listings, parish=id)
    
def get_listing(id=None):
    '''View a single listing'''
    if id is None:
        return redirect(url_for('all_listings'))
    else:
        listing = Listing.get_by_id(id)
        return render_template('listing.html', listing=listing)

@login_required
def landlord_landlord(id=None):
    '''Allows a user to landlord a landlord via email.'''
    landlord = Landlord.get_by_id(id)
    if landlord is None:
        flash(u'You must select a landlord to landlord','error')
        return redirect(url_for('all_listings'))
    form = LandlordForm()
    if form.validate_on_submit():
        if send_email(form, landlord.email_address, landlord.name):
            flash(u'Email sent!', 'success')
            return redirect(url_for('all_listings'))
        else:
            flash(u'Sending failed', 'error')
            return redirect(request.url)
        
    else:
        return render_template('landlord_landlord.html', form=form, landlord=landlord)
        
def warmup():
    '''App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    '''
    return ''

'''Helper methods below'''
def persist_listing(form, listing):
    '''persist a listing to the database'''
    listing.title = form.title.data
    listing.address = form.address.data
    listing.city = form.city.data
    listing.parish = form.parish.data
    listing.description = form.description.data
    listing.occupancy = form.occupancy.data
    listing.rent = float(form.rent.data)
    listing.landlord = Landlord.get_by_user(users.get_current_user())
    listing.user = users.get_current_user()
    if isinstance(form, EditListingForm):
        listing.occupied = form.occupied.data
    else:
        listing.occupied = False
    listing.put()
        
def send_email(form, to, name):
    recipient = "%s <%s>" % (name, to)
    subject = form.subject.data
    sender = "%s <%s>" % (form.name.data, users.get_current_user().email())
    body = form.body.data
    try:
        mail.send_mail(sender=sender, to=recipient, subject=subject, body=body)
        return True
    except:
        logging.error(traceback.extract_stack())
        return False