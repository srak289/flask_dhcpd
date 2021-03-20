from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mako import MakoTemplates
import os

app = Flask(__name__)

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dhcpd.db')
dhcp_path = '/var/lib/dhcpd/dhcpd.leases'
conf_path = '/etc/dhcp/dhcpd.conf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+path

db = SQLAlchemy(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.secret_key = os.urandom(16)

app.template_folder = 'templates'
mako = MakoTemplates(app)

from app import routes
