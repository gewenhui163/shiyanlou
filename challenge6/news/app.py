#!/usr/bin/env python3

import os, json
from flask import Flask, render_template, abort

app = Flask(__name__)

#json file
filesrc = os.path.abspath('..')+'/files/'
filelist = os.listdir(os.path.abspath('..')+'/files')
print(filelist)

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
	if os.path.exists(filesrc+filename):
		with open(filesrc+filename, 'r') as f:
				data = json.load(f)
		return render_template('file.html', data=data)
	else:
		abort(404)

app.run()
