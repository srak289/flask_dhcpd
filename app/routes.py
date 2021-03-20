from flask import request, redirect, url_for, session, send_file
from flask_mako import render_template
import os
import re

from app import app, db, dhcp_path, conf_path
from app.models import *

pages = {
    'Home':'/home',
    'Networks':'/networks',
    'Leases':'/leases',
    'Update':'/update',
}

html_escape_table = {
    '&': '&amp;',
    '"': '&quot;',
    "'": '&apos;',
    '>': '&gt;',
    '<': '&lt;'
}

def render_all(t, **kwargs):
    return render_template(t, **kwargs, pages=pages)

def strip(d):
    safe = {}
    for k, v in d.items():
        v = "".join(html_escape_table.get(c, c) for c in v)
        safe.update({k:v})

    return safe

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_all('index.html', content='lol')

@app.route('/networks')
def networks():
    networks = Network.query.all()
    return render_all('networks.html', networks=networks)

@app.route('/network/<int:id>')
def network(id):
    n = Network.query.filter_by(id=id).first()
    return render_all('network.html', n=n)

@app.route('/leases')
def leases():
    leases = Lease.query.all()
    return render_all('leases.html', leases=leases)

@app.route('/lease/<int:id>')
def lease(id):
    l = Lease.query.filter_by(id=id).first()
    return render_all('lease.html', l=l)

@app.route('/update')
def update():
    with open(dhcp_path, 'r') as f:
        data = f.read()
    res = [ x for x in re.split('[{}\n;]', data) if x != '' ]

    t_lease = Lease()
    
    t_obj = []
    t_dict = {}
    for i in res:
        t_str = i.split()
        k, v = t_str[0], t_str[1:]
        if type(v) is list:
            tmp = v
            v = ''
            for j in tmp:
                v += f'{j} ' 
        if k == 'lease' and 'lease' in t_dict.keys():
            t_obj.append(t_dict)
            t_dict = {}
            t_dict.update({k : v})
        else:
            if '-' in k:
                k = k[:k.index('-')]
            t_dict.update({k : v})
            
    for i in t_obj:
        t_lease = Lease()
        for k, v in i.items(): 
            t_lease.__dict__.update({k:v})
            db.session.add(t_lease)
    db.session.commit()

    with open(conf_path, 'r') as f:
        data = f.read()
    res = [ x for x in re.split('[{}\n\t;]', data) if not re.match('^\s*$', x) ]
    t_network = Network()
    t_obj = []
    t_dict = {}
    for i in res:
        t_str = i.split()
        k, v = t_str[0], t_str[1:]
        if type(v) is list:
            tmp = v
            v = ''
            for j in tmp:
                v += f'{j} ' 
        if k == 'lease' and 'lease' in t_dict.keys():
            t_obj.append(t_dict)
            t_dict = {}
            t_dict.update({k : v})
        else:
            if '-' in k:
                k = k[:k.index('-')]
            t_dict.update({k : v})
    print(t_dict)        
    #for i in t_obj:
    #    print(i)
    #    t_network = Network()
    #    for k, v in i.items(): 
    #        t_lease.__dict__.update({k:v})
    #        db.session.add(t_lease)
    #db.session.commit()

    return redirect(url_for('index'))
