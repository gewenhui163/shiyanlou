#!/usr/bin/env python3

import os, json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('files', lazy='dynamic'))
    
    def __init__(self, title, content, category, created_time=None):
        self.title = title
        self.content = content
        self.category = category
        if created_time is None:
            created_time = datetime.utcnow()
        self.created_time = created_time
        self.category = category

    def __repr__(self):
        return '<File %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def index():
        filelist = db.session.query(File.title).all()
        #print(filelist)
        return render_template('index.html', datalist=filelist)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.route('/files/<filename>')
def fileshow(filename):
        data = db.session.query(File).filter_by(title=filename).all()
        print('data:',data)
        if data:
                return render_template('file.html', data=data)
        else:
                abort(404)

#json file
#filesrc = os.path.abspath('..')+'/files/'
#filelist = os.listdir(os.path.abspath('..')+'/files')
#print(filelist)
'''
@app.route('/')
def index():
	if filelist:
		datalist = []
		for jsonfile in filelist:
			with open(filesrc+jsonfile, 'r') as f:
				data = json.load(f)
				data.update({'name':jsonfile})
				datalist.append(data)
				#print(datalist)
		return render_template('index.html', datalist=datalist)
	else:
		abort(404)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.route('/files/<filename>')
def fileshow(filename):
	if os.path.exists(filesrc+filename+'.json'):
		with open(filesrc+filename+'.json', 'r') as f:
				data = json.load(f)
		return render_template('file.html', data=data)
	else:
		abort(404)

'''
