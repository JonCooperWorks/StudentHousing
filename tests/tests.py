#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

TODO: These tests need to be updated to support the Python 2.7 runtime

"""
import os
import unittest

from google.appengine.ext import testbed

from application import app
from application import views, models

class ListingTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
        
    def setCurrentUser(self,email,user_id,is_admin=False):
        os.environ['USER_EMAIL'] or ''
        os.environ['USER_ID'] or ''
        os.environ['USER_IS_ADMIN'] = 1 if is_admin else '0'
        
    def test_home(self):
        rv = self.app.get('/')
        assert rv.status == '200 OK'
        
    def test_listing_loads(self):
        rv = self.app.get('/')
        assert 'All Listings' in rv.data
    
    def test_empty_listings(self):
        rv = self.app.get('/listings')
        assert 'No listings yet.' in rv.data
        
    def test_404(self):
        rv = self.app.get('/missing')
        assert rv.status == '404 NOT FOUND'
        assert '<h1>Not found</h1>' in rv.data

class MailTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def testMailSent(self):
        mail.send_mail(to='alice@example.com',
                       subject='This is a test',
                       sender='bob@example.com',
                       body='This is a test e-mail')
        messages = self.mail_stub.get_sent_messages(to='alice@example.com')
        self.assertEqual(1, len(messages))
        self.assertEqual('alice@example.com', messages[0].to)
    
if __name__ == '__main__':
    unittest.main()
