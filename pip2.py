# -*- coding: utf-8 -*-
"""pip2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jqniHXR91z0-qR9FNrCeLdpcLri3kIZT
"""

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
  json_respone ={
      'status_code' :200,
      'description' : "Menyapa Hello World",
      'data' : "Hello World"
  }

  respone_data  = jsonify(json_respone)
  return respone_data

if __name__== '__main__':
  app.run()

import re

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
  json_respone ={
      'status_code' :200,
      'description' : "Menyapa Hello World",
      'data' : "Hello World"
  }

  respone_data  = jsonify(json_respone)
  return respone_data

@app.route('/text', methods=['GET'])
def text():
  json_respone ={
      'status_code' :200,
      'description' : "Original Text",
      'data' : "Hello, apa kabar semua"
  }
  
  respone_data  = jsonify(json_respone)
  return respone_data

@app.route('/text-clean', methods=['GET'])
def text_clean():
  json_respone ={
      'status_code' :200,
      'description' : "Original Text",
      'data' : re.sub (r'[^A-Za-z0-9]', '', "Hello, apa kabar semua"),
  }
  
  respone_data  = jsonify(json_respone)
  return respone_data

if __name__== '__main__':
  app.run()