#!/usr/bin/env python3

import os, json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
#from pymongo import MongoClient
import pymongo
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

#connect mongodb database
#client = MongoClient('127.0.0.1', 27017)
#db_mongo = client.shiyanlou
client = pymongo.MongoClient('mongodb://localhost:27017/')
db_mongo = client.shiyanlou
collection = db_mongo.file

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

    def add_tag(self, tag_name):
        tag = {'fileid':self.id, 'tag':tag_name}
        #print(db_mongo)
        collection.insert_one(tag)
        #print(tag)

    def remove_tag(self, tag_name):
        collection.delete_one({'fileid':self.id, 'tag':tag_name})

    @property
    def tags(self):
        tagslist = collection.find({'fileid':self.id})
        print(tagslist)
        return tagslist

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def index():
        filelist = db.session.query(File).all()
        #print(filelist)
        #print(filelist[0].id)
        #tagslist = collection.find()
        newfilelist = []
        newfile = {}
        for file in filelist:
            print(file.id)
            filetags = collection.find({'fileid': file.id})
            filetag = []
            for tag in filetags:
                filetag.append(tag['tag'])
                #print(tag['tag'])
            #print('filetags:',filetag)
            newfile['id'] = file.id
            newfile['content'] = file.content
            newfile['tags'] = filetag
            newfile['title'] = file.title
            #file['tags'] = filetag
            print(newfile)
            newfilelist.append(newfile)
        print(newfilelist)
        return render_template('index.html', datalist=newfilelist)

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
