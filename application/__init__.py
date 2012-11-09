"""
Initialize Flask app

"""

from flask import Flask
import filters

app = Flask('application')
app.config.from_object('application.settings')
app.jinja_env.filters['bv2yn'] = filters.bv2yn
app.jinja_env.filters['int2parish'] = filters.int2parish
app.jinja_env.filters['int2occupancy'] = filters.int2occupancy
app.jinja_env.filters['tophonenum'] = filters.to_phone_number
import urls
