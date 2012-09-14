from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

#Contact me page
app.add_url_rule('/contact', 'contact_me', view_func=views.contact, methods=['GET', 'POST'])

#About page
app.add_url_rule('/about', 'about', view_func=views.about)

#Create an account
app.add_url_rule('/register', 'authenticate', view_func=views.authenticate, methods=['GET','POST'])


#View all listings
app.add_url_rule('/listings', 'all_listings', view_func=views.all_listings)

#View listings by parish
app.add_url_rule('/listings/parish/<int:id>', 'by_parish', view_func=views.listings_by_parish)
app.add_url_rule('/listings/parish', view_func=views.all_listings)

#Get a single listing
app.add_url_rule('/listing/<int:id>', 'get_listing', view_func=views.get_listing)

#Contact a landlord
app.add_url_rule('/contact/<int:id>', 'contact_landlord', view_func=views.contact_landlord, methods=['GET', 'POST'])

#Manage listings
app.add_url_rule('/manage', 'manage_listings', view_func=views.manage_listings)
app.add_url_rule('/manage/<int:id>', 'manage_listing', view_func=views.manage_listing, methods=['GET','POST'])

#Add a listing
app.add_url_rule('/listings/add', 'add_listing', view_func=views.add_listing, methods=['GET', 'POST'])

#Delete a listing
app.add_url_rule('/listings/delete/<int:id>', view_func=views.delete_listing, methods=['GET', 'POST'])

#Change contact info
app.add_url_rule('/dashboard/edit', 'update_contact', view_func=views.update_contact, methods=['GET', 'POST'])

#Dashboard
app.add_url_rule('/dashboard', 'profile', view_func=views.profile)

#Logout
app.add_url_rule('/logout', 'logout', view_func=views.logout)


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
